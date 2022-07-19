const {
  default: stream
} = require("./api/stream")

const iconList = [{
    "name": "电导率",
    "value": "icon-diandaoshuai"
  },
  {
    "name": "PH值",
    "value": "icon-PHzhi"
  },
  {
    "name": "含氧量",
    "value": "icon-hanyangliang"
  }, {
    "name": "水位",
    "value": "icon-shuiwei"
  },
  {
    "name": "库容",
    "value": "icon-kurong"
  },
  {
    "name": "浊度",
    "value": "icon-zhuodu"
  },
  {
    "name": "溶解氧",
    "value": "icon-rongjieyang"
  },
  {
    "name": "压力",
    "value": "icon-yali"
  },
  {
    "name": "悬浮物",
    "value": "icon-xuanfuwu"
  },
  {
    "name": "流量",
    "value": "icon-liuliang"
  },
  {
    "name": "水温",
    "value": "icon-shuiwen"
  },
  {
    "name": "土壤水分",
    "value": "icon-turangshuifen"
  },
  {
    "name": "土壤湿度",
    "value": "icon-turangshidu"
  },
  {
    "name": "风速",
    "value": "icon-fengsu"
  },
  {
    "name": "电源电压",
    "value": "icon-dianyuandianya"
  },
  {
    "name": "CO2浓度",
    "value": "icon-CO2nongdu"
  },
  {
    "name": "大气压",
    "value": "icon-daqiya"
  },
  {
    "name": "光合辐射",
    "value": "icon-guanghefushe"
  },
  {
    "name": "结露",
    "value": "icon-jielou"
  },
  {
    "name": "空气温度",
    "value": "icon-kongqiwendu"
  },
  {
    "name": "空气湿度",
    "value": "icon-kongqishidu"
  },
  {
    "name": "风向",
    "value": "icon-fengxiang"
  },
  {
    "name": "降雨量",
    "value": "icon-jiangyuliang"
  },
  {
    "name": "露点温度",
    "value": "icon-loudianwendu"
  },
  {
    "name": "光照强度",
    "value": "icon-guangzhaoqiangdu"
  },
  {
    "name": "蒸发量",
    "value": "icon-zhengfaliang"
  },
  {
    "name": "总辐射",
    "value": "icon-zongfushe"
  }, {
    "name": "光照时间",
    "value": "icon-guangzhaoshijian"
  },
  {
    "name": "PM2.5",
    "value": "icon-PM25"
  },
  {
    "name": "小时降雨量",
    "value": "icon-xiaoshijiangyuliang"
  },
  {
    "name": "风力",
    "value": "icon-fengli"
  },
  {
    "name": "硫化氢",
    "value": "icon-liuhuaqing"
  },
]
const colorList = [
  "bg-red",
  "bg-orange",
  "bg-yellow",
  "bg-olive",
  "bg-green",
  "bg-cyan",
  "bg-blue",
  "bg-purple",
  "bg-mauve",
  "bg-pink",
  "bg-brown",
  "bg-grey",
  "bg-black",
  "bg-gray",
  "bg-red light",
  "bg-orange light",
  "bg-yellow light",
  "bg-olive light",
  "bg-green light",
  "bg-cyan light",
  "bg-blue light",
  "bg-purple light",
  "bg-mauve light",
  "bg-pink light",
  "bg-brown light",
  "bg-grey light",
  "bg-gradual-red",
  "bg-gradual-orange",
  "bg-gradual-green",
  "bg-gradual-purple",
  "bg-gradual-pink",
  "bg-gradual-blue",
]
const streamTypeList = [{
    name: '整型（int）',
    value: 'int'
  },
  {
    name: '浮点型（float）',
    value: 'float'
  },
  {
    name: '布尔型（bool）',
    value: 'bool'
  },
  {
    name: '字符型（char）',
    value: 'char'
  }
]
const qosList = [{
    name: '0',
    value: 0
  },
  {
    name: '1',
    value: 1
  },
  {
    name: '2',
    value: 2
  }
]
module.exports = {
  iconList,
  colorList,
  qosList,
  streamTypeList,
}