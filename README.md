Predicting TikTok video engagement using trending metadata
==============================

Project Organization

Sprint 1

In Sprint 1, I mainly focused on setting up the project and making sure I understood the problem I wanted to solve. My goal for this capstone is to figure out what influences engagement on trending TikTok videos using the metadata that gets scraped from the platform. I spent time looking through the raw JSON data, identifying which fields looked useful, and planning out how I would clean and analyze it later. This sprint was more about organizing the project structure (using cookiecutter), confirming the dataset I would use, and outlining the direction I wanted the project to go. It helped me see that the data was definitely workable and that the project was realistic.

Sprint 2

Sprint 2 was where I actually started working with the data. I built a full cleaning script that loads the raw trending.json file, flattens the nested fields, handles missing values, and creates new features like caption length, hashtag count, engagement, and engagement rate. This gave me a clean dataset to use for analysis.
After cleaning, I created an EDA notebook to explore the data. I looked at distributions, correlations, and relationships between different variables. The biggest takeaway was that play count has the strongest connection to engagement, especially when plotted on a log scale. Caption length and hashtag count didn’t show meaningful relationships with engagement, which surprised me because I expected hashtags to matter more. Overall, Sprint 2 helped me understand the dataset on a deeper level and showed me which features might actually be useful for modeling. It also gave me a clearer idea of what challenges I’ll face going into Sprint 3, especially with the data being so skewed toward viral videos.

Sprint 3

In Sprint 3, I focused on building and evaluating predictive models for TikTok video engagement. Using the cleaned dataset from Sprint 2, I created baseline, linear regression, and random forest regression models to compare performance and understand which features drive engagement. I split the data into training and test sets and evaluated models using RMSE, MAE, and R². The baseline and linear regression models performed poorly, confirming that engagement is not well explained by linear relationships alone. The random forest model performed significantly better and captured nonlinear patterns in the data. Feature importance analysis showed that play count overwhelmingly dominates engagement prediction, while caption length, hashtag count, video duration, and verification status contribute only marginally. These results align closely with the exploratory findings from Sprint 2.

------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
