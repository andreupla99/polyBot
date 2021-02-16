# PolyBot

For this project we will be makeing a Python bot capable of creating and working with convex polygons. To do so, we will need three main things: a polygon class to manage the polygons, a compiler to undestand the commands we will be using and a [Telegram bot](https://core.telegram.org/bots) to interact with the system.

## Requirements

In order to be able to execute polyBot you will need to have *python3* and *pip3* installed. Once you have both you can run the following command:

    pip3 install -r requirements.txt

This will ensure you have the correct versions of *antlr4*, *pillow* and the [*Telegram bot api*](https://core.telegram.org/bots) installed. The other libraries we will be using, such as math or random, are python implicit libraries.

Once you have all the requirements installed, you can run:

    python3 bot.py

This will run the bot, now you will need to head to Telegram and open the bot at t.me/andreuplaPolyBot and run the /start command to begin with your execution.
Once you are done, you must interrupt the execution from terminal.

If you want a reference for the kind of commands that can be used, there is a file called "example.txt" that has a few examples. You can execute them and observe the results, then modify as you please.

## Part 1: Class for convex polygons
  
First and foremost we will need some way to work with polygons. To do so we need to create specific data structures that allow us to represent the values that define a polygon, and allow us to operate with them.

### Polygon class

The *Polygon()* class will allow us to do just that. The first atribute we find is *polygons*, which is simply a list containing the instances of those polygons with names we have declared previously, so that we can find them afterwards. Then we have the private class atributes containing the basic information of each polygon, such as the vertices (represented as a list of pairs), the name (if it has one), the color, the number of vertices and the number of vertices. For convenience, every time a polygon is iniciated it is converted to the greatest convex polygon possible in order not to have issues with later operations.

For some of the atributes we have their getter and setter function, but for some others it is omitted as it was not required for the use given. If we were to add more functionalities we could easily add them later. 

Next up we have the *checkConvex* class, which allows us to check wether or not a polygon is convex, and *checkRegular*, which checks if we have a regular polygon. This will be useful before or after some operations in order to check if they can be done or to avoid converting a non-convex polygon to a convex one if not needed, or simply to return if we have a need for it.

Then we have both *pointInPoly* and *polyInPoly*, which allow us to determine wether a point is inside a polygon or not or, by recursion of the first, wether a polygon is inside a polygon.

The functions *perimeterLength* and *areaPoly* return both the length and area of a polygon respectively.

The function *getCentroid* computes and returns the centroid of the polygon (point where the center of mass is).

The function *showVertices* returns a string representing the vertices of the polygon at hand using the output format required.

The function *boundingBox* returns a polygon represented by four vertices that defines the bounding box of the polygon given. Notice that this function works with just one polygon, as required, but it could also be adapted to work with various polygons.

The function *makeConvex* returns a convex polygon, ordered so that the first vertix is the one with the lowest y value, and in case of a tie the one with the lowest x.

The function *correctCoords* returns the largest convex polygon possible that can be made by the given vertices (already stored in the polygon). This polygon will contain inside all the other points not included in the polygon definition, although they will not be shown. This is done using [Graham's scan method](https://en.wikipedia.org/wiki/Graham_scan).

Finally the function *getPoly* returns an instance of the polygon that is stored in the global variable polygons, given its name and assuming that there exists a polygon with such name.

#### Auxiliary functions to the polygon class

The *Polygon* class is not alone in this program. We have also implemented auxiliary functions that allow us both to execute specific tasks or to be called from the bot directly.

To begin with, we have the classes *distance*, *areaTriangle*, *pointsToVec* and *getAngle*, which are basic operations with points and vectors that allow us to get basic information.

Then we have the functions *union* and *intersection*, which compute and return the resulting polygon of the respective union or intersection between the two polygons given. These functions make use of the functions *findIntersectionPoint* and *findIntersectingVertices* in order to determine the points where the vertices or edges from both polygons colide, creating and adding them if necessary for the computation of the resulting polygon.

Next up we have *drawPolygons*, which draws the given list of polygons in the first paramiter on the file specified in the second paramiter. This function recursively calls for every polygon given the function *drawPolygon*, which divides each polygon into its different components (vertices and edges), and paints them using *drawPoint* and *drawLine* respectively. Then *drawPixel* is used in both *drawPoint* and *drawLine* functions to modify the specific pixels necessary to correctly represent the polygons.

The function *mergeSortVertices* is an auxiliary function to *correctCoords*, and is no more than a custom merge sort made to fit the data types used.

Finally we have the auxiliary function *genRandomPoly*, which allow us to create x random points where x is determined by the paramiter given. Then the largest possible convex polygon is created with the given points, and those that do not fit are omitted.

## Part 2: A programming language to work with convex polygons

### TreeVisitor class

TreeVisitor is a class that allow us to understand the instructions given by the telegram api, with the help of the parser and the visitor, and of course the grammar declaration we have done. 

In here we define for each part of each kind of instruction what we have to do with the information given. This class communicates with the *polygon* class in order to obtain the information needed, and always returns it as a string list to the *bot* class. This makes it so the bot always gets a string and can decide either to show the string or, in case of pictures, show the picture.

### Interpreter

For the interpreter we use the class *Inreptret*, which has the simple job of collecting the commands send by the [Telegram bot](https://core.telegram.org/bots) and seding them to the lexer and parser to generate the corresponding tree, which we can then send to the *TreeVisitor* for interpretation and execution.

### Grammar

Finally, we have defined a specific grammar to be able to understand the input given by the [Telegram bot](https://core.telegram.org/bots) and work with it accordingly. The definition of this grammar is stored in the file "Poly.g".

## Part 3: A bot to interact with convex polygons

### Bot class

The bot class is the one in charge of recieving the messages from Telegram and returning the outputs. It also allows us to show information with the commands we have defined, such as a guide to execute operations with polygons or information about the author.


### Comments

Due to python file depencencies i have not managed to put the files in the different folders "bot" and "cl", so i will have them all in the same folder.

## Author

* **Andreu Pla** 

## References

* [Enunciat](https://github.com/jordi-petit/lp-polimomis-2020)
* [antlr4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md#windows)
* [Graham's scan method](https://en.wikipedia.org/wiki/Graham_scan)
* [Telegram bot](https://core.telegram.org/bots)
* [Properties of convex polygons](https://es.wikipedia.org/wiki/Pol%C3%ADgono_convexo)

