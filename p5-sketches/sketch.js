let seed;

let config

function setup() {
  config = new Config({seed});
  config.setSeed();
  createCanvas(config.canvasWidth, config.canvasHeight, SVG);
  angleMode(RADIANS);
  ellipseMode(RADIUS);

  let saveArtButton = createButton("save");
  saveArtButton.mouseClicked(saveArt);

  noLoop();
}

function draw()
{
  for(let i =0; i < 10; i++){
    circle(random(config.canvasWidth), random(config.canvasHeight), random(5,20))
  }
  
}


function saveArt() {
  console.log("saving Svg");
  save(config.name(), "svg");
}
