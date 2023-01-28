
# DO NOT EDIT THIS FILE - GENERATED FROM 02_ts_utils.ipynb

import tensorflow as tf
import tensorflow.keras as keras
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle
import ts_utils

#--------------------------------------------------------------------------------
def plot(y, yh, x=None, title="", scaler=None):
    if (scaler):
        y1  = scaler.inverse_transform(y) 
        yh1 = scaler.inverse_transform(yh) 
    else:
        y1, yh1 = y, yh

    x = x or range(max(len(y1),len(yh)))
    
    plt.scatter(x, y1,  marker='.', s=64, edgecolor='k', label="Y")
    plt.scatter(x, yh1, marker='x', s=64, edgecolor='k', label="$\hat{y}$")
    plt.title(title)
    plt.grid(1)
    plt.legend()

#--------------------------------------------------------------------------------
def plotFeatureImportance(weights, labels):
    plt.bar( x = range(len(weights)), height=weights)
    if (labels):
        print(labels)
        axis = plt.gca()
        axis.set_xticks(range(len(labels)))
        axis.tick_params(axis='both', which='major', labelsize=15)

        _ = axis.set_xticklabels(labels, rotation=90)


#--------------------------------------------------------------------------------
def eval_performance(model, trn_dataset, tst_dataset=None, metric_name="loss"):
    en = model.evaluate(trn_dataset)
    if (tst_dataset):
        et = model.evaluate(tst_dataset);
    else:
        et = [0] * len(en)

    mi = max(0, model.metrics_names.index(metric_name))

    return np.array(en).flat[mi], np.array(et).flat[mi]

performance = {}
def plot_performance(models, trn_dataset, tst_dataset=None, metric_name="loss", performance = {}, reeval=0):
    for m in models:
        if (not reeval and performance.get(m.name, None)):
            print(f"Performance for {m.name} exists")
            continue;  # Dont evaluate if performance is already computed

        performance[m.name] = eval_performance(m, trn_dataset, tst_dataset, metric_name)

    if (len(performance) <= 0 ):
        print("No models to plot?")

    x = np.arange(len(performance))
    width = 0.3
    val_mae =  [v[0] for v in performance.values()]
    test_mae = [v[1] for v in performance.values()]

    plt.title(f"Comparisons of '{metric_name}' : ")
    plt.ylabel('Metrics')
    plt.bar(x - 0.17, val_mae, width,  label= f'Training {metric_name}')
    plt.bar(x + 0.17, test_mae, width, label= f'Test {metric_name}')
    plt.xticks(ticks=x, labels=performance.keys(), rotation=45)
    _ = plt.legend()
    
    return performance

#--------------------------------------------------------------------------------
def plot_predictions(ydf, yhatdf, start=0, end=1024*1024, title=""):
    plt.figure(figsize=(14, 4))

    for c in ydf.columns:
        y1, p1 = ydf[c][start:end], yhatdf[c][start:end]
        plt.scatter( y1.index, y1, edgecolors='k', marker='o', label= f'{c}: y',    c='#2ca02c' )
        plt.scatter( p1.index, p1, edgecolors='k', marker='X', label= f'{c}: yhat', c='#ff7f0e')

        plt.title = title
        plt.legend()
        plt.show()


#--------------------------------------------------------------------------------
def predict_and_plot( model, window_trn, window_tst, howmany=1024* 1024,
                        plot_start=0, plot_end=1024*1024, df=None, scaler=None, label_slice=None):
    y, yhat = None, None
    y, yhat = ts_utils.model_predict( model , window_trn,  y, yhat, howmany)
    if (window_tst is not None):
        y, yhat = ts_utils.model_predict( model , window_tst,  y, yhat, howmany)

    if ( df is not None):
        ydf = ts_utils.inverse_transform(y, scaler, label_slice, df)
        pdf = ts_utils.inverse_transform(yhat, scaler, label_slice, df)
    else:
        ydf = pd.DataFrame(y   )
        pdf = pd.DataFrame(yhat)

    plot_predictions(ydf,pdf, plot_start, plot_end, title=f"{model.name}")

    return ydf, pdf