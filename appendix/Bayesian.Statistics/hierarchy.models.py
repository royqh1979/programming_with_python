import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
import seaborn as sns
#import warnings
#warnings.filterwarnings("ignore", category=FutureWarning)

trials = 10;
successes = 5

# Set up model context
with pm.Model() as coin_flip_model:
    # Probability p of success we want to estimate
    # and assign Beta prior
    p = pm.Beta("p", alpha=1, beta=1)

    # Define likelihood
    obs = pm.Binomial("obs", p=p, n=trials,
                      observed=successes,
                      )

    # Hit Inference Button
    idata = pm.sample()

import arviz as az

az.plot_posterior(idata, show=True);