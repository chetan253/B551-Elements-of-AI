# Image Classification using KNN, Adaboost and Neural Networks

### Problem Statement:
The task was to classify the images based on the rotation factor i.e. if they are rotated by 0, 90, 180, 270 degrees.

### About data
The data comprised of nearly 40000 images as training set and 1000 images as testing set.
The data has been tansformed to image space vectors of 192 dimensions (8x8x3)rgb

### Accuracies Obtained on test set:
KNN : 67.97%
Adaboost : 70.89%
Neural Network : 71.04%

#### Run Instructions:
Note: The program outputs the model file in the training phase with the respective weights required for any of the algorithms aforementioned and takes that model as input during the testing phase.

Train phase:
```python orient.py tr ain train-data.txt [output_model_filename] [model_name]```

Testing phase:
```python orient.py test test-data.txt [input_model_filename] [model_name]```

The output of testing will be stored in output_[model_name].txt file 
