# Requirements
- python 2.7.18  (due to Scanner API incompatibilities, will not work on python 3)  
- pyside2 for GUI

My advice is that, whichever library you choose, you make a data structure for your polygons that suits your algorithms so that they can be more simple and readable rather then try to get these algorithms to manipulate a canvas directly. Then you can write the code that draws them separate (i.e. independent) of the main logic.


https://www.learnpyqt.com/courses/custom-widgets/bitmap-graphics/