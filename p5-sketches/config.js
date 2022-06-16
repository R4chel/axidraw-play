function Config({seed, debug, canvasName, canvasWidth, canvasHeight}) {
    this.debug = debug === undefined ? false : debug;
    this.seed = seed === undefined ? (debug ? 1 : seed) : seed;
    this.canvasName = canvasName === undefined ? "sketch" : canvasName;
    this.canvasWidth = canvasWidth === undefined ? (debug ? 200 : 500) : canvasWidth;
    this.canvasHeight = canvasHeight === undefined ? (debug ? 200 : 500) : canvasHeight;


    this.setSeed = function () {
        if (this.seed === undefined) {
            this.seed = round(random(1000000));
        }
        randomSeed(this.seed);
    }

    this.name = function() { 
        return config.canvasName 
        + "--seed-" + config.seed
    }
}