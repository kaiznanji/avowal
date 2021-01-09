link = """
<html>
<style>
    .toolbarbutton {
        width: 50px;
    }

    .header {
        padding: 1px;
        text-align: center;
        background: #1abc9c;
        color: white;
        font-size: 20px;
    }

    #left {
        width: 750px;
        float: left;
    }

    html,
    body {
        height: 100%;
        margin: 0;
    }

    body {
        background: skyblue;
    }

    p {
        font-size: 40px;
        font-family: georgia, cursive;
    }

    a {
        font-size: 16px;
        font-family: georgia, cursive;
    }
</style>

<script type="text/javascript">

    /*
    Some variables, including a canvas for drawing, a drawing context for
    the canvas, a flag (boolean) to indicate drawing, x and y points for drawing, and a
    final flag (dot_flag, boolean) to support starting a new stroke by clearing contents.
    */
    var canvas, drawdiv, ctx, flag = false,
        prevX = 0,
        currX = 0,
        prevY = 0,
        currY = 0,
        dot_flag = false;

    /*
    Horrible variable names: Do as I do, not as I say. x is your drawing color and y is the 
    stroke width when drawing. So a black stroke that is 2 pixels wide.
    */
    var x = "black",
        y = 2;

    /*
    function init gets called on launch. It sets up the drawing context for the canvas, ctx and
    it adds "listeners" to the canvas to allow the canvast to receive mouse events. Mouse events 
    will be handled by a function findxy. Note that findxy gets two aprameters, the "event", i.e. 
    was it a move, a mousedown, a mouseup, or a mouseout event, and the event parameters, "e" which
    has useful things like x,y components of the mouse.
    */
    function init() {
        canvas = document.getElementById('can');
        drawdiv = document.getElementById('sketch');
        ctx = canvas.getContext("2d");
        w = canvas.width;
        h = canvas.height;

        canvas.addEventListener("mousemove", function (e) {
            findxy('move', e)
        }, false);
        canvas.addEventListener("mousedown", function (e) {
            findxy('down', e)
        }, false);
        canvas.addEventListener("mouseup", function (e) {
            findxy('up', e)
        }, false);
        canvas.addEventListener("mouseout", function (e) {
            findxy('out', e)
        }, false);
    }

    /*
    This helper function gets contents from the Clipboard. It will typically prompt you for 
    permission to read from the clipboard. When it gets content from the clipboard, it will 
    paste it into the points list and it will draw the points on the screen.
    */
    async function getClipboardContents() {
        try {
            const text = await navigator.clipboard.readText();
            document.getElementById("points").textContent = text;
            draw_all();
        } catch (err) {
            console.error('Failed');
        }
    }

    /*
    A helper function which draws a line from the previous (x,y) point to the current (x,y) point.
    */
    function draw() {
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
        ctx.lineTo(currX, currY);
        ctx.strokeStyle = x;
        ctx.lineWidth = y;
        ctx.stroke();
        ctx.closePath();
        document.getElementById("points").textContent += '[' + currX + ', ' + currY + '],';
    }

    /*
    This function is a bit complex. It basically parses a list of points and draws the 
    entire list of points. It does this by filling an "array", a "list" in racket using
    a strong parsing function that strips everything out of the string except numbers
    (that's the allpoints = mystring ... line) and then goes through and draws all of 
    those points (that's the for loop).
    */
    function draw_all() {
        var mystring = document.getElementById("points").textContent;
        var allpoints = mystring.match(/(\+|-)?((\d+(\.\d+)?)|(\.\d+))/g).map(Number);
        if ((allpoints.length > 1) && ((allpoints.length % 2) == 0)) {
            var i;
            ctx.beginPath();
            ctx.moveTo(allpoints[0], allpoints[1]);
            for (i = 1; i < (allpoints.length / 2); i++) {
                ctx.lineTo(allpoints[2 * i], allpoints[2 * i + 1]);
                ctx.strokeStyle = x;
                ctx.lineWidth = y;
                ctx.stroke();
            }
            ctx.closePath();
            create_image()
        }
    }

    /*
    Clear everything.
    */
    function erase() {
        ctx.clearRect(0, 0, w, h);
        document.getElementById("canvasimg").style.display = "none";
        document.getElementById("answer").textContent = '';
    }

    /*
    Copies the points drawn on the display to the clipboard. You can use this to then paste your list of points into Dr Racket.
    */
    function copy() {
        document.getElementById("points").select();
        document.execCommand('copy');
    }

    /*
    A past wrapper function. Calls the getClipboardContents function to do the work.
    */
    function paste() {
        erase();
        getClipboardContents();
    }

    /*
    Creates a small image of the stroke you have drawn. You can use your Racket code to create
    a recognizer for any set of gestures you want (e.g. the numbers 1 to 10, etc.). If you do this
    you might want little "images" that you can paste somewhere to show people what the gestures
    your recognizer accepts look like.
    */
    function create_image() {
        document.getElementById("canvasimg").style.border = "2px solid";
        var dataURL = canvas.toDataURL();
        document.getElementById("canvasimg").src = dataURL;
        document.getElementById("canvasimg").style.display = "inline";
    }

    /*
    this is the function that handles mouse events. Basically it reads as follows:
    1. If the event is a mousedown event (the user presses down on the mouse button),
    then we clear the rectangle and start a new points list. We also set previous x and y
    to the current position, and we get ready to draw a line by setting our flags to true.
    We also create a small dot, a rectangle, of size 2, 2 at the current point on the 
    beginning of the line. 
    2. If the even is up or out (i.e. we released the mouse button or moved out of the
    region), then we want to stop drawing. We also show the image of what was drawn.
    3. Otherwise, it is a mousemove function. If we are drawing (i.e. the flag is true, set 
    on mouse down, the first if statement above), then we set our points and call the draw 
    function.
    */
    function findxy(res, e) {
        if (res == 'down') {
            ctx.clearRect(0, 0, w, h);
            document.getElementById("points").textContent = '[';
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - (canvas.offsetTop + drawdiv.offsetTop - window.pageYOffset);

            flag = true;
            dot_flag = true;
            if (dot_flag) {
                ctx.beginPath();
                ctx.fillStyle = x;
                ctx.fillRect(currX, currY, 2, 2);
                ctx.closePath();
                dot_flag = false;
            }
        }
        if (res == 'up' || res == "out") {
            if (flag) {
                document.getElementById("points").textContent += ']';
                create_image();
            }
            flag = false;
        }
        if (res == 'move') {
            if (flag) {
                prevX = currX;
                prevY = currY;
                currX = e.clientX - canvas.offsetLeft;
                currY = e.clientY - (canvas.offsetTop + drawdiv.offsetTop - window.pageYOffset);
                draw();
            }
        }
    }

    function inspect() {
        var val = document.getElementById("points").textContent;

        fetch('/compute', {

            // Declare what type of data we're sending
            headers: {
                'Content-Type': 'application/json'
            },

            // Specify the method
            method: 'POST',

            // A JSON payload
            body: JSON.stringify({ "gesture": val })
        })
            .then(function (response) {
                return response.text();
            })
            .then(function (text) {

                document.getElementById("answer").textContent = text;
            });
    }



</script>



<body onload="init()">
    <div class='header'>
        <p>AVOWAL</p>
        <form action="https://github.com/kaiznanji/avowal">
            <input style="width:100px;" type="submit" value="View Code" />
        </form>
    </div>
    <div id='intro' style="position:relative;">
        <h1></h1>
        <img src="static/graffitialphabet.png"
            style="position:absolute;top:250;left:50;border:1px solid;" />
    </div>
    <div id="sketch" style="position:relative">
        <div style="text-align:center;"><b>Draw With Mouse Here</b></div>
        <canvas id="can" width="400" height="400" style="position:absolute;top:50;left:700;border:2px solid;"></canvas>
        <button type="button" onclick=inspect() style="position:absolute;top:575;left:700;">Classify Drawing</button>
        <input type="button" class="toolbarbutton" value="Clear" id="clr" size="23" onclick="erase()"
            style="position:absolute;top:575;left:810;">
        <textarea readonly id="points" name="points" rows="30" cols="30" style="display:none;"></textarea>
        <div style="position:absolute;top:30;left:1200;">Sample Picture</div>
        <textarea readonly id="answer" rows="3" cols="25"
            style="position:absolute;top:470;left:700;border:1px solid;font-size: 18pt;"></textarea>
        <img id="canvasimg" style="position:absolute;top:50;left:1200;" width="100 style=" display:none;">
        <div style="position:absolute;top:75;left:50;width:600px;"><a>The following full-stack web application allows
                you to classify letters using
                the Palm Pilot Graffit Set. It uses javascript to compute the drawings into vectorized form and a python
                script to classify the vectors as letters. Click the
                button link under the title to take you to my Github page where you can see the code for the
                application!
                <p>
                    Below is the graffiti set used to classify your drawings. Use the drawing template on the right and
                    hit classify drawing to do the work!

            </a></div>
    </div>
</body>

</html>
"""