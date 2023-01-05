var option = {
  tooltip: {
    trigger: 'axis',
    valueFormatter: (value) => value.toFixed(2)
  },
  xAxis: {
    name: '时间',
    nameGap: 5,
    type: 'time',
  },
  yAxis: {
    type: 'value',
    nameGap: 10,
  },
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 100
    },
    {
      start: 0,
      end: 100
    }
  ],
  series: [
    {
      name: 'Mock Data',
      type: 'line',
      smooth: true,
      symbol: 'none',
      areaStyle: {},
      data: [],
    }
  ],
  grid: {
    top : 40,
    bottom: 40,
  },
}

module.exports = {
  ...option
}