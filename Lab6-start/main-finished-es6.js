//21522755 - Nguyễn Mạnh Tuấn
// setup canvas
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const width = (canvas.width = window.innerWidth);
const height = (canvas.height = window.innerHeight);

// Ball count display
const ballCountDisplay = document.querySelector("p");
let ballCount = 0;

// function to generate random number
function random(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Shape constructor
function Shape(x, y, velX, velY) {
    this.x = x;
    this.y = y;
    this.velX = velX;
    this.velY = velY;
    this.exists = true;
}

// Ball constructor
function Ball(x, y, velX, velY, exists, color, size) {
    Shape.call(this, x, y, velX, velY);
    this.color = color;
    this.size = size;
    this.exists = exists;
}

// Set prototype chain and constructor
Ball.prototype = Object.create(Shape.prototype);
Ball.prototype.constructor = Ball;

// Ball methods
Ball.prototype.draw = function () {
    ctx.beginPath();
    ctx.fillStyle = this.color;
    ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
    ctx.fill();
};

Ball.prototype.update = function () {
    if (this.x + this.size >= width || this.x - this.size <= 0) {
        this.velX = -this.velX;
    }
    if (this.y + this.size >= height || this.y - this.size <= 0) {
        this.velY = -this.velY;
    }
    this.x += this.velX;
    this.y += this.velY;
};

Ball.prototype.collisionDetect = function () {
    for (let j = 0; j < balls.length; j++) {
        if (!(this === balls[j]) && balls[j].exists) {
            const dx = this.x - balls[j].x;
            const dy = this.y - balls[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < this.size + balls[j].size) {
                balls[j].color = this.color =
                    `rgb(${random(0, 255)}, ${random(0, 255)}, ${random(0, 255)})`;
            }
        }
    }
};

// EvilCircle constructor
function EvilCircle(x, y, exists) {
    Shape.call(this, x, y, 20, 20);
    this.color = "white";
    this.size = 10;
    this.exists = exists;
}

// Set prototype chain and constructor
EvilCircle.prototype = Object.create(Shape.prototype);
EvilCircle.prototype.constructor = EvilCircle;

// EvilCircle methods
EvilCircle.prototype.draw = function () {
    ctx.beginPath();
    ctx.strokeStyle = this.color;
    ctx.lineWidth = 3;
    ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
    ctx.stroke();
};

EvilCircle.prototype.checkBounds = function () {
    if (this.x - this.size < 0) this.x = this.size;
    if (this.x + this.size > width) this.x = width - this.size;
    if (this.y - this.size < 0) this.y = this.size;
    if (this.y + this.size > height) this.y = height - this.size;
};

EvilCircle.prototype.setControls = function () {
    let _this = this;
    window.onkeydown = function (e) {
        if (e.key === "a") {
            _this.x -= _this.velX;
        } else if (e.key === "d") {
            _this.x += _this.velX;
        } else if (e.key === "w") {
            _this.y -= _this.velY;
        } else if (e.key === "s") {
            _this.y += _this.velY;
        }
    };
};

EvilCircle.prototype.collisionDetect = function () {
    for (let j = 0; j < balls.length; j++) {
        if (balls[j].exists) {
            const dx = this.x - balls[j].x;
            const dy = this.y - balls[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < this.size + balls[j].size) {
                balls[j].exists = false;
                ballCount--;
                ballCountDisplay.textContent = `Ball count: ${ballCount}`;
            }
        }
    }
};

// Generate balls
let balls = [];
while (balls.length < 25) {
    const size = random(10, 20);
    let ball = new Ball(
        random(size, width - size),
        random(size, height - size),
        random(-7, 7),
        random(-7, 7),
        true,
        `rgb(${random(0, 255)}, ${random(0, 255)}, ${random(0, 255)})`,
        size
    );
    balls.push(ball);
    ballCount++;
    ballCountDisplay.textContent = `Ball count: ${ballCount}`;
}

// Create EvilCircle
const evilCircle = new EvilCircle(width / 2, height / 2, true);
evilCircle.setControls();

// Animation loop
function loop() {
    ctx.fillStyle = "rgba(0, 0, 0, 0.25)";
    ctx.fillRect(0, 0, width, height);

    for (const ball of balls) {
        if (ball.exists) {
            ball.draw();
            ball.update();
            ball.collisionDetect();
        }
    }

    evilCircle.draw();
    evilCircle.checkBounds();
    evilCircle.collisionDetect();

    requestAnimationFrame(loop);
}

loop();