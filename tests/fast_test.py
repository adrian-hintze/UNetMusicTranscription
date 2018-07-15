'''
created: 2018-05-31
edited: 2018-07-04
author: Adrian Hintze @Rydion
'''

import shutil
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from tf_unet.unet import Unet, Trainer
from tf_unet.image_util import ImageDataProvider

#plt.rcParams['image.cmap'] = 'gist_earth'

IMAGE_FORMAT = '.bmp'
TRAINING_DATA_DIR = './data/preprocessed/MIREX/*'
data_suffix = '_in' + IMAGE_FORMAT
mask_suffix = '_out' + IMAGE_FORMAT
EPOCHS = 20

def train():
    data_provider = ImageDataProvider(
        TRAINING_DATA_DIR,
        data_suffix = data_suffix,
        mask_suffix = mask_suffix
    )

    '''
    x, y = data_provider(1)
    fig, ax = plt.subplots(1, 3, figsize = (12, 4))
    ax[0].imshow(x[0, ..., 0], aspect = 'auto')
    ax[1].imshow(y[0, ..., 1], aspect = 'auto', cmap = plt.cm.gray)
    plt.draw()
    plt.show()
    
    print(np.shape(x))
    print(np.shape(y))
    print(np.amin(x))
    print(np.amax(x))
    print(np.amin(y))
    print(np.amax(y))
    print(data_provider.channels)
    print(data_provider.n_class)
    '''
    #return

    net = Unet(
        channels = data_provider.channels,
        n_class = data_provider.n_class,
        layers = 3,
        features_root = 16
    )
    trainer = Trainer(
        net,
        optimizer = 'momentum',
        opt_kwargs = dict(momentum = 0.2)
    )
    path = trainer.train(
        data_provider,
        './unet_trained_fast',
        prediction_path = './prediction_fast',
        epochs = EPOCHS,
        display_step = 2
    )

    return net, data_provider

def predict(net, data_provider):
    x, y = data_provider(1)
    prediction = net.predict('./unet_trained_fast/model.ckpt', x)
    mask = np.zeros(np.shape(prediction), dtype = np.float32)
    mask[:, :, 0] = prediction[:, :, 0] >= 0.5
    mask[:, :, 1] = prediction[:, :, 1] >= 0.5

    print(np.shape(x))
    print(np.shape(y))
    print(np.shape(prediction))
    print(np.shape(mask))
    print(np.amin(x))
    print(np.amax(x))
    print(np.amin(y))
    print(np.amax(y))
    print(np.amin(prediction))
    print(np.amax(prediction))
    print(np.amin(mask))
    print(np.amax(mask))

    fig, ax = plt.subplots(1, 4, figsize = (12, 4))
    ax[0].imshow(x[0, ..., 0], aspect = 'auto')
    ax[1].imshow(y[0, ..., 1], aspect = 'auto', cmap = plt.cm.gray)
    ax[2].imshow(prediction[0, ..., 1], aspect = 'auto', cmap = plt.cm.gray)
    ax[3].imshow(mask[0, ..., 1], aspect = 'auto', cmap = plt.cm.gray)
    ax[0].set_title("Input")
    ax[1].set_title("Ground truth")
    ax[2].set_title("Prediction")
    ax[3].set_title("Mask")
    plt.draw()
    plt.show()

def test():
    net, data_provider = train()
    predict(net, data_provider)

def init():
    #tf.reset_default_graph()

    shutil.rmtree('./unet_trained_fast', ignore_errors = True)
    shutil.rmtree('./prediction', ignore_errors = True)

def main():
    init()
    test()

if __name__ == '__main__':
    main()
