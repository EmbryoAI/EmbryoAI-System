# -*- coding: utf8 -*-

class PatientBaseInfo():
    
    def __init__(self, id, idcardNo, idcardTypeId, patientName, birthdate, country, locationId, address, email, mobile, createTime, updateTime, delFlag, isDrinking, isSmoking):
        self.id = id
        self.idcardNo = idcardNo
        self.idcardTypeId = idcardTypeId
        self.patientName = patientName
        self.birthdate = birthdate
        self.country = country
        self.locationId = locationId
        self.address = address
        self.email = email
        self.mobile = mobile
        self.createTime = createTime
        self.updateTime = updateTime
        self.delFlag = delFlag
        self.isDrinking = isDrinking
        self.isSmoking = isSmoking

    