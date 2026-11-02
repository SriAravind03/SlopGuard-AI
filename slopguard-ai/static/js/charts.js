const canvas = document.querySelector('#quality-chart');
if (canvas && window.Chart) {
  const values = JSON.parse(canvas.dataset.values);
  new Chart(canvas, {type:'radar',data:{labels:['Repetition','Information density','Redundancy','Vocabulary diversity','AI-like patterns'],datasets:[{data:values,label:'Score / 100',backgroundColor:'rgba(145,108,255,.18)',borderColor:'#a38bff',pointBackgroundColor:'#5ee0c5',borderWidth:2}]},options:{plugins:{legend:{display:false}},scales:{r:{min:0,max:100,ticks:{color:'#8290aa',backdropColor:'transparent',stepSize:25},grid:{color:'rgba(151,164,191,.14)'},angleLines:{color:'rgba(151,164,191,.14)'},pointLabels:{color:'#c7d0e2',font:{family:'Manrope'}}}}}});
}
