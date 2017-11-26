# Animation code
import pymel.core as pm
import time
import pymel.core.datatypes as dt

def listNodes(node, list):
    list.append(node)
    children = node.getChildren()
    for child in children:
        listNodes(child, list)
        
def parents(node, matrix, list, referenceList):
    if node in referenceList:
        list.append(matrix)
    newMatrix = node.getRotation().asMatrix() * matrix
    children = node.getChildren()
    for child in children:
        parents(child, newMatrix, list, referenceList)
        
def main(jointList, newJointList, hip, newHip):

    first = pm.findKeyframe(hip, which='first')
    last = pm.findKeyframe(hip, which='last')
    
    pm.setCurrentTime(0)
    
    parentList = []
    targetParentList = []
        
    parents(hip, dt.Matrix(), parentList, jointList)
    parents(newHip, dt.Matrix(), targetParentList, newJointList)
    
    i = 0
    a = 0
    
    identityMatrix = dt.Matrix()
    identityMatrix2 = dt.Matrix()
    
    while i < len(jointList):
        
        curr = first
        
        pm.setCurrentTime(0)
    
        pyJoint = pm.PyNode(jointList[i])
        targetJoint = pm.PyNode(newJointList[i])
        parentJoint = parentList[i]
        targetParentJoint = targetParentList[i]
        
        bindPoseInverse = pyJoint.getRotation().asMatrix().inverse()
        bindPose = pyJoint.getRotation().asMatrix()
        bindPoseTarget = targetJoint.getRotation().asMatrix()
    
        while curr <= last:
            curr = pm.findKeyframe(hip, time=curr, which='next')
            pm.setCurrentTime(curr)
            
            if i == 0:
               k =  pyJoint.getRotation().asMatrix() * bindPoseInverse
               
               kPrim = identityMatrix.setToIdentity().inverse() * k * identityMatrix2.setToIdentity()
               
               kPrim2 = parentList[i] * kPrim * parentList[i].inverse()
               
               final = bindPoseTarget * kPrim2
               
               targetJoint.setRotation(dt.degrees(dt.EulerRotation(final)))
                        
               targetJoint.setTranslation(pyJoint.getTranslation())
               
               pm.setKeyframe(targetJoint)
            else:
            ####################################HIP DONE###########################################
                
                bodyK = bindPoseInverse * pyJoint.getRotation().asMatrix()
                
                bodykPrim = parentList[i].inverse() * bodyK * parentList[i]
                
                bodykPrim2 =  targetParentList[i] * bodykPrim * targetParentList[i].inverse()
                
                bodyFinal =  bindPoseTarget * bodykPrim2
                
                targetJoint.setRotation(dt.degrees(dt.EulerRotation(bodyFinal)))
                
                pm.setKeyframe(targetJoint)
    
            
            # apply key values
            if curr==last:
                i = i + 1
                break   
