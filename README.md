# gif-rotate
<br>
Still things to do with this, but for now, works as long as you specify the proper/correct parameters.<br>
<br>
<p>Python 3 script to spin an image on its y-axis or yz-axis by the specified number of degrees.
<p>Must specify input file, output file, and temporary directory to store images that make the animated gif.
<p>Ideal height and width can be omitted, but will default to the original image size.
<p>Rotation degrees can also be omitted, but will default to 360 degrees.
<br>
<br>
EXAMPLE:<br>
python gif-rotate.py -i image.jpg -o animated.gif -d temp -r 360 -g 100 -h 100 -t y
<br>
<br>
This will create a 100 by 100 pixel animated gif of the image rotating 360 degrees on its y-axis.
