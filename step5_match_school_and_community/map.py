#coding=UTF-8

import csv
import json


# 点是否在外包矩形内
def isPoiWithinBox(poi, sbox, toler=0.0001):
	# sbox=[[x1,y1],[x2,y2]]
	# 不考虑在边界上，需要考虑就加等号
	if poi[0] > sbox[0][0] and poi[0] < sbox[1][0] and poi[1] > sbox[0][1] and poi[1] < sbox[1][1]:
		return True
	if toler > 0:
		pass
	return False


# 射线与边是否有交点
def isRayIntersectsSegment(poi, s_poi, e_poi):  # [x,y] [lng,lat]
	if s_poi[1] == e_poi[1]:  # 排除与射线平行、重合，线段首尾端点重合的情况
		return False
	if s_poi[1] > poi[1] and e_poi[1] > poi[1]:
		return False
	if s_poi[1] < poi[1] and e_poi[1] < poi[1]:
		return False
	if s_poi[1] == poi[1] and e_poi[1] > poi[1]:
		return False
	if e_poi[1] == poi[1] and s_poi[1] > poi[1]:
		return False
	if s_poi[0] < poi[0] and e_poi[1] < poi[1]:
		return False
	xseg = e_poi[0] - (e_poi[0] - s_poi[0]) * (e_poi[1] - poi[1]) / (e_poi[1] - s_poi[1])  # 求交
	if xseg < poi[0]:
		return False
	return True

#只适用简单多边形
def isPoiWithinSimplePoly(poi, simPoly, tolerance=0.0001):
	# 点；多边形数组；容限
	# simPoly=[[x1,y1],[x2,y2],……,[xn,yn],[x1,y1]]
	# 如果simPoly=[[x1,y1],[x2,y2],……,[xn,yn]] i循环到终点后还需要判断[xn,yx]和[x1,y1]
	# 先判断点是否在外包矩形内
	if not isPoiWithinBox(poi, [[0, 0], [180, 90]], tolerance):
		return False

	polylen = len(simPoly)
	sinsc = 0  # 交点个数
	for i in range(polylen - 1):
		s_poi = simPoly[i]
		e_poi = simPoly[i + 1]
		if isRayIntersectsSegment(poi, s_poi, e_poi):
			sinsc += 1

	return True if sinsc % 2 == 1 else  False

def isPoiWithinPoly(poi, poly, tolerance=0.0001):
	# 点；多边形三维数组；容限
	# poly=[[[x1,y1],[x2,y2],……,[xn,yn],[x1,y1]],[[w1,t1],……[wk,tk]]] 三维数组

	# 先判断点是否在外包矩形内
	if not isPoiWithinBox(poi, [[0, 0], [180, 90]], tolerance):
		return False

	sinsc = 0  # 交点个数
	for epoly in poly: #逐个二维数组进行判断
		for i in range(len(epoly) - 1):  # [0,len-1]
			s_poi = epoly[i]
			e_poi = epoly[i + 1]
			if isRayIntersectsSegment(poi, s_poi, e_poi):
				sinsc += 1
	return True if sinsc % 2 == 1 else  False