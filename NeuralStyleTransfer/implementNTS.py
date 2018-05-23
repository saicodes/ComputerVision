"""
This code was inspired by the deeplearning.ai CNN course's week 4 assignments

"""

import os
import sys
import scipy.io
import scipy.misc
from NeuralStyleTransfer import *
from .utils import *   



import tensorflow as tf
import numpy as np

cimage = cwd+"images/louvre_small.jpg"
simage = cwd+"images/monet.jpg"

url = "http://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat"
file_name = cwd+"pretrained-model/imagenet-vgg-verydeep-19.mat"


def init(num_iterations = 200, c_image = cimage, s_image=simage):
    
    download_if_not_exists(file_name, url)
	
    
    # load, reshape, and normalize our "content" image (the Louvre museum picture):
    content_image = scipy.misc.imread(c_image)
    content_image = reshape_and_normalize_image(content_image)

    #  load, reshape and normalize our "style" image (Claude Monet's painting):
    style_image = scipy.misc.imread(s_image)
    style_image = reshape_and_normalize_image(style_image)

    # load the vgg19 model
    model = load_vgg_model(cwd+"pretrained-model/imagenet-vgg-verydeep-19.mat")
 
    # Start interactive session
    sess = tf.InteractiveSession()
    sess.run(tf.initialize_all_variables())
    
    sess.run(model['input'].assign(style_image))

    # Compute the style cost
    J_style = style_loss_func(sess, model)

    # Assign the content image to be the input of the VGG model.  
    sess.run(model['input'].assign(content_image))

    # Compute the content cost
    J_content = content_loss_func(sess, model)

    # Total cost
    J = total_cost(J_content, J_style)

    # define optimizer 
    optimizer = tf.train.AdamOptimizer(2.0)

    # define train_step 
    train_step = optimizer.minimize(J)

    #sess, input_image, num_iterations, model, train_step, J, J_content, J_style = input_value
    input_image = generate_noise_image(content_image)
    
    # Initialize global variables (you need to run the session on the initializer)
    ### START CODE HERE ### (1 line)
    sess.run(tf.initialize_all_variables())
    ### END CODE HERE ###
    
    # Run the noisy input image (initial generated image) through the model. Use assign().
    ### START CODE HERE ### (1 line)
    sess.run(model['input'].assign(input_image))
    ### END CODE HERE ###
    
    
    for i in range(num_iterations):
        
        # Run the session on the train_step to minimize the total cost
        sess.run(train_step)
                
        # Compute the generated image by running the session on the current model['input']
        generated_image = sess.run(model['input'])
        
        # Print every 20 iteration.
        if i%20 == 0:
            Jt, Jc, Js = sess.run([J, J_content, J_style])
            print("Iteration " + str(i) + " :")
            print("total cost = " + str(Jt))
            print("content cost = " + str(Jc))
            print("style cost = " + str(Js))
                    
            # save current generated image in the "/output" directory
            save_image(cwd+"output/" + str(i) + ".png", generated_image)
    
    sess.close()

    # save last generated image
    save_image(cwd+'output/generated_image.jpg', generated_image)
    
    # Un-normalize the image so that it looks good
    image = generated_image + CONFIG.MEANS
    
    # Clip and Save the image
    image = np.clip(image[0], 0, 255).astype('uint8')
    
    return image

    