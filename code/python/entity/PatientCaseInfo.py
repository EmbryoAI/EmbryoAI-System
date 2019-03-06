# -*- coding: utf8 -*-

class PatientCaseInfo():
    
    def __init__(self, id, orgId, patientId, userId, patientAge, patientHeight, patientWeight, ecTime, ecCount, insemiTime, insemiTypeId, state, delFlag, medicalRecordNo, embryoScoreId, memo):
        self.id = id
        self.orgId = orgId
        self.patientId = patientId
        self.userId = userId
        self.patientAge = patientAge
        self.patientHeight = patientHeight
        self.patientWeight = patientWeight
        self.ecTime = ecTime
        self.ecCount = ecCount
        self.insemiTime = insemiTime
        self.insemiTypeId = insemiTypeId
        self.state = state
        self.delFlag = delFlag
        self.medicalRecordNo = medicalRecordNo
        self.embryoScoreId = embryoScoreId
        self.memo = memo

    