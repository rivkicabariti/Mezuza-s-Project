import numpy as np
from keras.models import load_model
from PIL import Image
from skimage import transform
import os
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import time
import image_quality as iq


def ConversionToCharachters(num: int):
    classes = ['other', 'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'ך', 'כ', 'ל', 'ם', 'מ', 'ן', 'נ', 'ס', 'ע',
               'ף', 'פ',
               'ץ', 'צ', 'ק', 'ר', 'ש', 'ת']
    return classes[num]


def To_classify(path):
    img = Image.open(str(path))
    # Small changes to the image in order to fit it to the model
    img = np.array(img).astype('float32')
    img = transform.resize(img, (28, 28, 1))
    img = np.expand_dims(img, axis=0)
    my_model = load_model("model_try3.h5")
    output = my_model.predict(img)
    i = np.argmax(output, axis=1)
    return ConversionToCharachters(int(i))



# *******************************
# בדיקת נכונות המודל, על פי תיקיית הולידטיון
def V():
    list_validation = []
    list_true = []
    # בגלל שבולידטיון יש 32 תמונות מכל אות נבנה רשימה של 32 פעמים מכל האותיות הנכונות
    for directory in os.listdir('db_letters/train_test_validate/validate'):
        for i in range(32):
            list_true.append(directory)
    # שליחת כל תמונה מהולידטיון לסיווג ושמירת תוצאת הסיווג שלה
    for directory in os.listdir('db_letters/train_test_validate/validate'):
        for image in os.listdir(fr'db_letters/train_test_validate/validate/{directory}'):
            list_validation.append(To_classify(fr'db_letters/train_test_validate/validate/{directory}/{image}'))

    y_true = list_true
    y_pred = list_validation
    cm = confusion_matrix(y_true, y_pred)  # שמירת מטריצת בלבול פשוטה בלי עיצובים

    class_names = ['other', 'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'ך', 'כ', 'ל', 'ם', 'מ', 'ן', 'נ', 'ס',
                   'ע', 'ף', 'פ',
                   'ץ', 'צ', 'ק', 'ר', 'ש', 'ת']
    # הצגת כל מדדי הדיוק
    print(classification_report(y_true, y_pred,
                                target_names=class_names))


# מעוצב
# https://stackoverflow.com/questions/39033880/plot-confusion-matrix-sklearn-with-multiple-labels
def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=False):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()


# plot_confusion_matrix(cm, class_names)
def extract_integer_from_line(filename):
    return int(((filename.split('.')[0]).split('e'))[1])


def extract_integer_from_letter(filename):
    if filename.startswith('l'):
        return int(((filename.split('.')[0]).split('r'))[1])
    else:
        return int('100')

def MainClassification(path):
    iq.main_change_size(path)
    dict={}
    for line in sorted(os.listdir(path),key=extract_integer_from_line):
        list = []
        for letter in sorted(os.listdir(fr'{path}/{line}'),key=extract_integer_from_letter):
            if letter.endswith('.png') or letter.endswith('.PNG') or letter.endswith('.jpg'):
                list.append(To_classify(fr'{path}/{line}/{letter}'))
                print(To_classify(fr'{path}/{line}/{letter}'))
        dict.update({line:list})
    return dict
