canvas = document.getElementById('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight - 50;
ctx = canvas.getContext('2d');
center = [canvas.width / 2, canvas.height / 2];
//center = [500, 300]
count_nodes_input = document.getElementById('count_nodes_input');
ok_btn = document.getElementById('btn');
power1_input = document.getElementById('power1');
power2_input = document.getElementById('power2');

var count_nodes = 0+count_nodes_input.value;
node_size = 10;
var links = [];
var edges = [];

var history = [];


var D = [
  [0, 100, 100],
  [100, 0, 100],
  [100, 100, 0]
]
var epsilon = 5e-10;
var coords = [];
var delta = [];
var start_pos = [];
var radius = 0.0;//node_size * Math.sqrt(count_nodes) * 2;


function redraw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < count_nodes; i++) {
    ctx.beginPath();
    ctx.arc(coords[i][1], coords[i][2], node_size, 0, 2*Math.PI, false);
    ctx.fillStyle = '#ff0000';
    ctx.fill();
    ctx.closePath();
  }

  ctx.strokeStyle = '#000000';
  ctx.beginPath();
  for (let i = 0; i < edges.length; i++) {
    for (let j = 0; j < edges[i].length; j++) {
      //links.push([i, edges[i][j]])
      ctx.moveTo(coords[i][1], coords[i][2]);
      let x = coords[edges[i][j]][1];
      let y = coords[edges[i][j]][2];
      ctx.lineTo(x, y);
    }
  }
  ctx.stroke();
  ctx.closePath();
}

function abssum(matrix) {
  let r = 0.;

  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[i].length; j++)
      r += Math.abs(matrix[i][j]);
  }

  return r;
}


function nullate_matrix(arr) {
  for (let x = 0; x < arr.length; x++) {
    for (let y = 0; y < arr[x].length; y++)
      arr[x][y] = 0.
  }
  
  return arr;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function iterate1(power1=500000, power2=1e-1) {
  var power = power1
  //отталкивание частиц
  for (let epoch = 0; epoch < 10000; epoch++) {
    for (let i = 0; i < count_nodes; i++) {
      /*
      let x = coords[i][1];
      let y = coords[i][2];

      let dist = Math.sqrt(Math.pow(x - center[0], 2) + Math.pow(y - center[1], 2));
      let vx = (x - center[0]) / dist;
      let vy = (y - center[1]) / dist;

      delta[i][0] -= vx * power / dist;
      delta[i][1] -= vy * power / dist;
      */
      for(let j = i + 1; j < count_nodes; j++) {
        if (i == j)
          continue;
        
        let x1 = coords[i][1];
        let y1 = coords[i][2];
        let x2 = coords[j][1];
        let y2 = coords[j][2];
        
        let dist = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
        let vx = (x2 - x1) / dist;
        let vy = (y2 - y1) / dist;
        
        let coef = Math.pow(dist, 2) * (i*i + 1);

        delta[i][0] -= vx * power / coef;
        delta[i][1] -= vy * power / coef;
        delta[j][0] += vx * power / coef;
        delta[j][1] += vy * power / coef;
      }
    }
    //притягивание нитей
    for (let ind = 0; ind < links.length; ind++) {
      let node1 = links[ind][0]
      let node2 = links[ind][1]
      let x1 = coords[node1][1]
      let y1 = coords[node1][2]
      let x2 = coords[node2][1]
      let y2 = coords[node2][2]

      let dist1 = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
      let dist2 = Math.sqrt(Math.pow(start_pos[node1][0] - start_pos[node2][0], 2) 
                            + Math.pow(start_pos[node1][1] - start_pos[node2][1], 2));
      
      let vx = (x2 - x1) / dist1;
      let vy = (y2 - y1) / dist1;

      let coef = power2*Math.abs((dist2 - dist1)) / (ind*ind + 1)
      delta[node1][0] += vx * power * coef;
      delta[node1][1] += vy * power * coef;
      delta[node2][0] -= vx * power * coef;
      delta[node2][1] -= vy * power * coef;
    }
    //draw vectors
    // for(let i = 0; i < count_nodes; i++) {
    //   ctx.moveTo(coords[i][1], coords[i][2]);
    //   ctx.lineTo(coords[i][1] + 10*delta[i][0], coords[i][2] + 10*delta[i][1])
    //   ctx.stroke();
    //   ctx.font = "30px Arial";
    //   ctx.fillText(coords[i][1] + 10*delta[i][0], coords[i][2] + 10*delta[i][1],
    //     '' + delta[i][0] + ' ' + delta[i][1])
    // }
    
    //обновляем координаты
    for (let i = 0; i < count_nodes; i++) {
      for (let j = 0; j < 2; j++) {
        let c = coords[i][j+1] + delta[i][j];
        if (c > radius && c < 2 * center[j] - radius)
          coords[i][j+1] = c;
        // coords[i][j+1] += delta[i][j];
        // if (coords[i][j+1] > 2*center[j] - radius)
        //   coords[i][j+1] = 2*center[j] - radius;
        // else {
        //   if (coords[i][j+1] < radius)
        //     coords[i][j+1] = radius;
        // }
      }
    }
    
    console.log('Abssum:', abssum(delta))
    if (abssum(delta) < epsilon)
      return;
    //обнуляем дельты
    delta = nullate_matrix(delta)
    
    //await sleep(1);
    redraw();
  }
}

async function iterate() {
  var sum_changes = 0.
  do {
    sum_changes = 0.
    for (let i = 0; i < count_nodes; i++) {
      for (let j = 0; j < count_nodes; j++) {
        if (i == j)
          continue;
        
        let dist = Math.sqrt(Math.pow(coords[i][1] - coords[j][1], 2) +
                            Math.pow(coords[i][2] - coords[j][2], 2))
        delta[i][0] += D[i][j]*(coords[i][1] - coords[j][1]) / dist
        delta[i][1] += D[i][j]*(coords[i][2] - coords[j][2]) / dist
        
        if (D[i][j] > 0) {
          delta[i][0] /= 0.1*D[i][j];
          delta[i][1] /= 0.1*D[i][j];
        }
      }
    }
    for (let i = 0; i < count_nodes; i++) {
      for (let j = 0; j < 2; j++)
        coords[i][j] += delta[i][j];
    }
    sum_changes = abssum(delta);
    delta = nullate_matrix(delta);
    console.log('Chages:', sum_changes)
    await sleep(1);
    redraw();
  } while(sum_changes > epsilon);
}

ok_btn.onclick = () => {
  count_nodes = 0+count_nodes_input.value;
  radius = node_size * Math.sqrt(count_nodes) * 2;
  power1 = 0. + power1_input.value
  power2 = 0. + power2_input.value
  node_size /= Math.log10(count_nodes)

  for (let i = 0; i < count_nodes; i++) {
    var rand_int = Math.floor(Math.random() * count_nodes);
    while(rand_int == i)
      rand_int = Math.floor(Math.random() * count_nodes);
    edges.push([rand_int]);
    links.push([i, rand_int])
  }
  
  for (let i = 0; i < count_nodes; i++) {
    coords.push([i, center[0] + radius*Math.cos(2*Math.PI*i/count_nodes), 
                center[1] + radius*Math.sin(2*Math.PI*i/count_nodes)]);
    start_pos.push([center[0] + radius*Math.cos(2*Math.PI*i/count_nodes), 
                center[1] + radius*Math.sin(2*Math.PI*i/count_nodes)]);
    // let a = Math.ceil(Math.random() * 1000);
    // let b= Math.ceil(Math.random() * 600);
    // coords.push([i, a, b]);
    // start_pos.push([i, a, b]);
    //coords.push([i, Math.ceil(Math.random() * 1000), Math.ceil(Math.random() * 600)]);
    delta.push([0., 0.])
  }

  redraw();
  iterate1(power1, power2);
}