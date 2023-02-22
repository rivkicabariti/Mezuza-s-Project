# Importing necessary functions
from keras.preprocessing.image import ImageDataGenerator,array_to_img, img_to_array, load_img
import os
from sklearn.model_selection import train_test_split
import shutil
# Initialising the ImageDataGenerator class.
# We will pass in the augmentation parameters in the constructor.
def image_augmantion(ori_path,k,dest_path):
    datagen = ImageDataGenerator(
        rotation_range=20,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False,
        brightness_range=(0.5, 1.5))

    # Loading a sample image
    img = load_img(ori_path)
    # Converting the input sample image to an array
    x = img_to_array(img)
    # Reshaping the input image
    x = x.reshape((1,) + x.shape)

    # Generating and saving 6 augmented samples
    # using the above defined parameters.
    i = 55
    for batch in datagen.flow(x, batch_size=1,save_to_dir=dest_path,save_prefix='0'+str(k)+str(i), save_format='png'):
        i += 1
        if i > 60:
            break


def TrainTestValidateSplit(path):
    X = []
    for file in os.listdir(path):
        current_path = os.path.join(path, file)
        for img in os.listdir(current_path):
            X.append(img)
        train_valid = path + '_train_valid'
        train = path + '_train'
        test = path + '_test'
        valid = path + '_valid'
        train_valid, test_name = train_test_split(X, test_size=0.2, random_state=42)
        train, valid = train_test_split(train_valid, test_size=0.1, random_state=42)
        for item in train:
            ori_path = current_path + '/' + item
            dest = fr'train_test_validate/train/{file}'
            shutil.copy(ori_path, dest)
        for item1 in test_name:
            ori_path = current_path + '/' + item1
            dest = fr'train_test_validate/test/{file}'
            shutil.copy(ori_path, dest)
        for item2 in valid:
            ori_path = current_path + '/' + item2
            dest = fr'train_test_validate/validate/{file}'
            shutil.copy(ori_path, dest)
        train_valid.clear()
        train.clear()
        test_name.clear()
        valid.clear()
        X.clear()

def changesInImages(path_to_db):
    for letter in os.listdir(path_to_db):
        i = 0
        for img in os.listdir(fr'{path_to_db}/{letter}'):
            image_augmantion(fr'{path_to_db}/{letter}/{img}',i,fr'{path_to_db}/{letter}')
            i += 1




