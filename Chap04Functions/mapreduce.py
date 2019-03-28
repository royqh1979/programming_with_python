"""

Originally taken from https://gist.github.com/georgepsarakis/7512023


"""
import collections
import itertools
import multiprocessing as mp
from functools import partial, reduce
from time import time
from typing import Iterable, Callable


class MapReducer(object):
    def __init__(self):
        self._workers = 0
        self._mapper = None
        self._prefilter = None
        self._postfilter = None
        self._reducer = None
        self._merger = None
        self._initial_value = None
        self._worker_assigner = None

    def workers(self, workers: int):
        """
        Set the number of processes

        :param workers: Number of processes to be spawned, 0 means all cpu cores
        :return: the MapReducer
        """
        if not isinstance(workers, int):
            raise ValueError("workers must be a positive integer!")
        if workers < 0:
            raise ValueError("workers must be a positive integer!")
        self._workers = workers
        return self

    def prefilter(self, prefilter: Callable = None):
        """
        set the function to filter items before mapping

        :param prefilter: function to filter items before entering map phase
        :return: the MapReducer
        """
        if not isinstance(prefilter, Callable):
            raise ValueError("the prefilter must is callable!")
        self._prefilter = prefilter
        return self

    def mapper(self, mapper: Callable):
        """
        Set the map function

        :param mapper: map function to apply to data items
        :return: the MapReducer
        """
        if not isinstance(mapper, Callable):
            raise ValueError("the mapper must is callable!")
        self._mapper = mapper
        return self

    def postfilter(self, postfilter: Callable):
        """
        set the filter to be use after mapping

        :param postfilter: the function to filter items after map phase
        :return: the MapReducer
        """
        if not isinstance(postfilter, Callable):
            raise ValueError("the postfilter must is callable!")
        self._postfilter = postfilter
        return self

    def reducer(self, reducer: Callable, initial_value):
        """
        set the reduce function

        :param reducer: function passed to reduce for the reduce phases (also the final phase)
        :param initial_value: the initial value used in reduce and the final merge phase
        :return: the MapReducer
        """
        if not isinstance(reducer, Callable):
            raise ValueError("the reducer must is callable!")
        self._reducer = reducer
        self._initial_value = initial_value
        return self

    def merger(self, merger: Callable):
        """
        set the reduce function used in the final merge phase

        :param merger: the reduce function used in the final merge phase
        :return: the MapReducer
        """
        if not isinstance(merger, Callable):
            raise ValueError("the reducer must is callable!")
        self._merger = merger
        return self

    def worker_assigner(self, worker_assigner: Callable):
        """
        set the function to assign items to workers

        :param worker_assigner: function to assign items to workers
        :return: the MapReducer
        """
        if not isinstance(worker_assigner, Callable):
            raise ValueError("the worker_assigner must is callable!")
        self._worker_assigner = worker_assigner
        return self

    def _process(self, items, manager):
        result = self._initial_value
        if self._prefilter is not None and self._postfilter is not None:
            for item in items:
                if not self._prefilter(item):
                    continue
                new_item = self._mapper(item)
                if not self._postfilter(item):
                    continue
                result = self._reducer(result, new_item)
        elif self._prefilter is None and self._postfilter is not None:
            for item in items:
                new_item = self._mapper(item)
                if not self._postfilter(item):
                    continue
                result = self._reducer(result, new_item)
        elif self._prefilter is not None and self._postfilter is None:
            for item in items:
                if not self._prefilter(item):
                    continue
                new_item = self._mapper(item)
                result = self._reducer(result, new_item)
        else:
            for item in items:
                new_item = self._mapper(item)
                result = self._reducer(result, new_item)
        manager.append(result)

    def __call__(self, data: Iterable):
        """
        process the data

        :param data: the data to be processed
        :return: the result
        """
        return self.run(data)

    def run(self, data: Iterable):
        """
        process the data

        :param data: the data to be processed
        :return: the result
        """
        if self._workers == 0:
            real_workers = mp.cpu_count()
        else:
            real_workers = self._workers

        if self._reducer is None:
            if self._prefilter is not None:
                data = filter(self._prefilter, data)
            data = mp.Pool(processes=real_workers).map(self._mapper, data)
            if self._postfilter is not None:
                data = filter(self._postfilter, data)
            return data

        if real_workers == 1:
            lst = []
            self._process(data, lst)
            return lst[0]

        m = mp.Manager()
        ''' manager object to store the result from all processes '''
        _results = m.list()
        processes = []
        ''' setup processes '''
        for worker_id in range(real_workers):
            ''' if the length of the iterable is known slice the iterable and assign to each worker '''
            if self._worker_assigner is None:
                P = mp.Process(target=self._process,
                               args=(itertools.islice(data, worker_id, None, real_workers), _results))
            else:
                ''' 
                create a partial since we need to pass the worker count and 
                current worker id to the assignment filter 
                '''
                assignment = partial(self._worker_assigner, real_workers, worker_id)
                ''' otherwise filter elements with worker_assign '''
                P = mp.Process(target=self._process,
                               args=(filter(assignment, data, ), _results))
            processes.append(P)
        ''' start & run '''
        [p.start() for p in processes]
        [p.join() for p in processes]
        ''' final reduce phase '''
        itemlist = itertools.chain(_results)
        result = self._initial_value
        if self._merger is not None:
            for item in itemlist:
                result = self._merger(result,item)
        else:
            for item in itemlist:
                result = self._reducer(result, item)
        return result
