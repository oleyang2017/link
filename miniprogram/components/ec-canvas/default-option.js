var option = {
  tooltip: {
    trigger: 'axis',
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
      name: 'Fake Data',
      type: 'line',
      smooth: true,
      symbol: 'none',
      areaStyle: {},
      data: [],
    }
  ],
  grid: {
    top : 40,
    bottom: 40, // 如果开启缩放会导致画面重叠要移除此配置，
  },
}

module.exports = {
  ...option
}