# -*- coding: cp949 -*-
import numpy as np
import cv2

def saveCamCalibration():
    termination = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((7*10, 3), np.float32)
    objp[:,:2] = np.mgrid[0:7, 0:10].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []

    cap = cv2.VideoCapture(1)
    count = 0
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (7, 10), None)

        if ret:
            objpoints.append(objp)
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), termination)
            imgpoints.append(corners)

            cv2.drawChessboardCorners(frame, (7, 10), corners, ret)
            count += 1
            print('[%d]' %count)

        cv2.imshow('img', frame)

        k = cv2.waitKey(0)
        if k == 27:
            break

        if count > 15:
            break

    cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    np.savez('calib.npz', ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

    print('ī�޶� Ķ���극�̼� �����͸� �����߽��ϴ�.')

saveCamCalibration()
