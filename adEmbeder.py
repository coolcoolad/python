import cv2 as cv
import os, time

appName = 'cctvf'
newAppName = 'adembeder'
m3u8Ext = '.m3u8'
streamName = 'test'

def tranformFile(fileName):
  #os.system('cp -f '+appName+'/'+fileName+' '+newAppName+'/'+fileName)
  #return
  vc = cv.VideoCapture(appName+'/'+fileName)
  width = int(vc.get(cv.CAP_PROP_FRAME_WIDTH))   
  height = int(vc.get(cv.CAP_PROP_FRAME_HEIGHT))
  fourcc = int(vc.get(cv.CAP_PROP_FOURCC))
  fps = vc.get(cv.CAP_PROP_FPS)
  vw = cv.VideoWriter(newAppName+'/'+'tmp.mp4', cv.VideoWriter_fourcc(*'avc1'), fps, (width, height))
  for i in range(int(vc.get(cv.CAP_PROP_FRAME_COUNT))):
    ret, img = vc.read()
    #img=cv.vconcat([img,img])
    if ret:
      vw.write(img)
  vc.release()
  vw.release()
  #os.system('ffmpeg -i '+newAppName+'/tmp.mp4 -bsf:v h264_mp4toannexb -codec copy '+newAppName+'/'+fileName+' > /dev/null 2>&1')
  os.system('ffmpeg -i '+newAppName+'/tmp.mp4 -bsf:v h264_mp4toannexb -codec copy -hls_time 100 -hls_list_size 0 '+newAppName+'/output.m3u8'+' > /dev/null 2>&1')
  os.system('cp '+newAppName+'/output0.ts '+newAppName+'/'+fileName)
  vc = cv.VideoCapture(newAppName+'/'+fileName)
  duration = vc.get(cv.CAP_PROP_POS_MSEC)
  frameCount = int(vc.get(cv.CAP_PROP_FRAME_COUNT))
  duration = frameCount/fps
  print(duration)
  vc.release()

def deleteFiles(fileSet):
  for fileName in fileSet:
    os.remove(newAppName+'/'+fileName)

def deleteOldFile(fileName):
  sequence = int(fileName[fileName.rfind('-')+1:-3])
  toDelete = fileName[:fileName.find('-')+1] + str(sequence-3) + '.ts'
  if os.path.exists(toDelete):
    os.system('rm -rf '+newAppName+'/'+toDelete)

def getPeriodArr(periodQueue):
  ret = []
  for line in periodQueue:
    #print(line[line.rfind(':')+1:-1])
    #print(line)
    period = float(line[line.rfind(':')+1:-1])
    ret.append(period)
  return ret

def getSequenceArr(fileQueue):
  ret = []
  for line in fileQueue:
    sequence = int(line[line.rfind('-')+1:-3])
    ret.append(sequence)
  return ret
    
def updateM3u8File(fileQueue, periodQueue):
  fileName = newAppName+'/'+streamName+m3u8Ext
  maxPeriod = int(max(getPeriodArr(periodQueue)))+1
  minSequence = getSequenceArr(fileQueue)[0]
  with open(fileName, 'w') as f:
    f.write('#EXTM3U\n')
    f.write('#EXT-X-VERSION:3\n')
    f.write('#EXT-X-MEDIA-SEQUENCE:'+str(minSequence)+'\n')
    f.write('#EXT-X-TARGETDURATION:'+str(maxPeriod)+'\n')
    for i in range(len(fileQueue)):
      f.write(periodQueue[i]+'\n')
      f.write(fileQueue[i]+'\n')
  #with open(fileName, 'r') as f:
  #  for line in f.readlines():
  #    print(line.strip())

def main():
  os.system('rm -rf '+newAppName+'/*')
  lastModifyTime = 0
  fileQueue = []
  periodQueue = []
  m3u8Path = appName+'/'+streamName+m3u8Ext
  if os.path.exists(m3u8Path) == False:
    print 'no m3u8'
    return
  lastWriteTime = time.time()
  while True:
    #modifyTime = os.path.getmtime(m3u8Path)
    #if modifyTime > lastModifyTime:
    lines = []
    with open(m3u8Path, 'r') as m3u8File:
      lines = m3u8File.readlines()
    
    period = ''
    for line in lines:
      line = line.strip()
      if line.startswith('#EXTINF'):
        period = line;
      if line.endswith('.ts'):
        fileName = line
        if fileName not in fileQueue:
          #t = time.time()
          tranformFile(fileName)
          #print(time.time()-t)
          print(period)
          fileQueue.append(fileName)
          periodQueue.append(period)
          if len(fileQueue) > 6:
            del(fileQueue[0])
            del(periodQueue[0])
          deleteOldFile(fileName)
          periodFloat = float(period[period.rfind(':')+1:-1])
          offset = periodFloat - (time.time() - lastWriteTime)
          if offset < 0:
            print('transform video to slow')
            return
          time.sleep(offset)
          print('offset: '+str(offset))
          #t = time.time()
          updateM3u8File(fileQueue, periodQueue)
          print(time.time() - lastWriteTime)
          lastWriteTime = time.time()
      #delta = modifyTime - lastModifyTime
      #print('delta: '+str(delta))
    #lastModifyTime = modifyTime


if __name__ == '__main__':
  main()
