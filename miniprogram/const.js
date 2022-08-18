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
const deviceImageList = [
  'IntelligentPower.png', 'EnergyConsumption.png', 'Internet.png', 'Wifi.png', 'DigitalCamera.png', 'CPU.png', 'EnvironmentalMonitoring.png', 'Devices.png', 'SmartWater.png', 'Research.png', 'NFCTechnology.png', 'Smartphone.png', 'WirelessHeadset.png', 'SmartTimer.png', 'MPPlayer.png', 'SmokeSensor.png', 'CCTV.png', 'SmartMicrowave.png', 'DroneDelivery.png', 'BluetoothSpeaker.png', 'EbookReader.png', 'SmartSIM.png', 'SmartMeter.png', 'HandheldConsole.png', 'GamingConsole.png', 'SmartWashingMachine.png', 'IntelligentEnergyControl.png', 'SmartHome.png', 'SmartGlasses.png', 'ElectricCar.png', 'SmartFridge.png', 'CDPlayer.png', 'WirelessPrinter.png', 'FitnessTracker.png', 'SmartWatch.png', 'ProcessingPower.png', 'SmartProductManagement.png', 'Mobility.png', 'Robotics.png', 'VRTechnology.png', 'SmartTV.png'
]
const permissionsMap = {
  view_device: "查看设备",
  change_device: "修改设备",
  delete_device: "删除设备",
  control_device: "控制设备",
  subscribe_topic: "订阅设备数据",
}
const inviteTypeList = [{
    name: '设备',
    value: 'device'
  },
  {
    name: '群组',
    value: 'group'
  },
]
module.exports = {
  iconList,
  colorList,
  deviceImageList,
  permissionsMap,
  inviteTypeList,
}