import cv2 as cv
import os, time

appName = 'cctvf'
newAppName = 'adembeder'
m3u8Ext = '.m3u8'
streamName = 'test'

def tranformFile(fileName):
  vc = cv.VideoCapture(appName+'/'+fileName)
  width = int(vc.get(cv.CAP_PROP_FRAME_WIDTH))   
  height = int(vc.get(cv.CAP_PROP_FRAME_HEIGHT))
  fourcc = int(vc.get(cv.CAP_PROP_FOURCC))
  vw = cv.VideoWriter(newAppName+'/'+fileName, cv.VideoWriter_fourcc(*'avc1'), vc.get(cv.CAP_PROP_FPS), (width, height * 2))
  for i in range(int(vc.get(cv.CAP_PROP_FRAME_COUNT))):
    ret, img = vc.read()
    img=cv.vconcat([img,img])
    if ret:
      vw.write(img)
  vc.release()
  vw.release()
  print(fileName+' ok')

def deleteFiles(fileSet):
  for fileName in fileSet:
    os.remove(newAppName+'/'+fileName)
    
def updateM3u8File(lines):
  #os.system('cp -f '+appName+'/'+streamName+m3u8Ext+' '+newAppName+'/'+streamName+m3u8Ext)
  fileName = newAppName+'/'+streamName+m3u8Ext
  with open(fileName, 'w') as f:
    for line in lines:
      f.write(line)

def main():
  os.system('rm -rf '+newAppName+'/*')
  lastModifyTime = 0
  fileExistingSet = set([])
  m3u8Path = appName+'/'+streamName+m3u8Ext
  if os.path.exists(m3u8Path) == False:
    print 'no m3u8'
    return
  while True:
    modifyTime = os.path.getmtime(m3u8Path)
    if modifyTime > lastModifyTime:
      lines = []
      with open(m3u8Path, 'r') as m3u8File:
        lines = m3u8File.readlines()
      
      newSet = set([])
      for line in lines:
        if line.strip().endswith('.ts'):
          fileName = line.strip()
          newSet.add(fileName)
          if fileName not in fileExistingSet:
            t = time.time()
            tranformFile(fileName)
            print(time.time()-t)
            fileExistingSet.add(fileName)
      toDeleteSet = fileExistingSet - newSet
      deleteFiles(toDeleteSet)
      fileExistingSet = newSet
      updateM3u8File(lines)
    delta = modifyTime - lastModifyTime
    print(time.gmtime(delta))
    lastModifyTime = modifyTime
    #time.sleep(0.5)


if __name__ == '__main__':
  main()
