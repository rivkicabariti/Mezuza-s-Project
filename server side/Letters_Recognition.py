
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout,Flatten,Conv2D, MaxPooling2D


class ModelTraining:

    @staticmethod
    def load_model():
        # create generator
        datagen = ImageDataGenerator()
        # load and iterate training dataset
        train_it = datagen.flow_from_directory(
        r'db_letters\train_test_validate\train',
        class_mode='categorical', color_mode="grayscale",
        batch_size=63693, target_size=(28, 28))

        # load and iterate test dataset
        test_it = datagen.flow_from_directory(
        r'db_letters\train_test_validate\test',
        class_mode='categorical',
        batch_size=4206,
        target_size=(28, 28), color_mode="grayscale")

        # confirm the iterator works
        X_train, y_train = train_it.next()
        X_test, y_test = test_it.next()
        # normalize inputs from 0-255 to 0-1
        X_train = X_train / 255
        X_test = X_test / 255

        num_classes = y_test.shape[1]
        return X_train, y_train, X_test, y_test, num_classes

    @staticmethod
    def baseline_model(num_classes):
        # Create a layer type model
        model = Sequential()
        # convolution layer: 32 filters, 3*3, use with relu for activation function
        #ה32 בהתחלה זה מספר הפילטרים,
        # כלומר הצורות השונות שבה המודל מסתכל על התמונה, אחד יותר יזהה אלכסון השני קו מאונך וכו
        #התוצאה היא סידרה של ייצוגים שונים של התמונה – כל פילטר יצר ייצוג שונה ולפיכך
        # במקרה שלנו יצרנו 32 ייצוגים שונים של תמונה.
        #ה3,3 זה הגרעין זה על כל כמה פיקסלים הוא מסתכל כל פעם
        model.add(Conv2D(32, (3, 3), input_shape=(28, 28, 1), activation='relu'))
        # [add this layer to decrease the loss]
        model.add(Conv2D(52, (3, 3), input_shape=(28, 28, 1), activation='relu'))
        model.add(Conv2D(64, (3, 3), input_shape=(28, 28, 1), activation='relu'))
        #תפקידה של שכבה זאת הוא לצמצם את המטריצה (ריבוע של הפיקסלים) שממדיו 2*2
        # פיקסלים שנמסר לה מהשכבה הקודמת לרבע, כלומר המטריצה תצומצם לפיקסל בודד.
        # זה נעשה על ידי דגימת הערך הגבוה מבין ארבעת הפיקסלים שמרכיבים את המטריצה
        # שהתקבלה ואותו היא מעבירה לשכבה הבאה.

        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(90, (3, 3), input_shape=(28, 28, 1), activation='relu'))
        model.add(Conv2D(95, (3, 3), input_shape=(28, 28, 1), activation='relu'))
        model.add(Conv2D(98, (3, 3), input_shape=(28, 28, 1), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # ignore from 20% from the noironim
        model.add(Dropout(0.2))
        # we have 3 chanels. flat them to one long vector
        model.add(Flatten())
        #הסיווג בפעול של התמונות נעשה ע"י רשת נוירונית מסוג Dense .
        # another noirinim layer (with activation function)
        model.add(Dense(128, activation='relu'))
        # output
        model.add(Dense(28, activation='softmax'))
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.summary()
        return model

    @staticmethod
    def fit_model(model, X_train, y_train, X_test, y_test):
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=25, batch_size=64, verbose=2)
        model.save("model_try3.h5")

    @staticmethod
    def buildModel():
        X_train, y_train, X_test, y_test, num_classes = network.load_model()
        model = network.baseline_model(num_classes)
        network.fit_model(model, X_train, y_train, X_test, y_test)


if __name__ == "__main__":
    network = ModelTraining()
    network.buildModel()