function deepCopy(obj){
  let objStr = JSON.stringify(obj)
  return JSON.parse(objStr);
}    

module.exports = {
  deepCopy
}