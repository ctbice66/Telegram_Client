def getDateRange():

	#starting points
	startYear			= int(input('Start Year: '))
	startMonth			= int(input('Start Month (1-12): '))
	startDay			= int(input('Start Day: '))
	endYear				= int(input('End Year: '))
	endMonth			= int(input('End Month (1-12): '))
	endDay				= int(input('End Day: '))
	partialStartMonth	= getPartialStartMonth(startMonth, startDay)
	partialEndMonth		= getPartialEndMonth(endMonth, endDay, getLeap(endYear))

	#list of days per month per year
	dateRange 			= []

	#list of years
	years 				= []

	#list of years
	for year in range(endYear - startYear + 1):
		if startMonth >= 1 and startDay >= 1:
			years.append(startYear + year)
		elif endMonth >= 1 and endDay >= 1:
			years.append(startYear + year)
		else:
			years.append(startYear)

	#build date range
	for year in years:
		#start year and end year
		if year == startYear and year == endYear:
			#single day
			if startYear == endYear and startMonth == endMonth and startDay == endDay:
				getMonth(dateRange, year, startMonth, True, True, startDay, endDay)
			#start month partial, end month partial
			elif partialStartMonth == True and partialEndMonth == True:
				#single month
				if endMonth == startMonth:
					getMonth(dateRange, year, startMonth, True, True, startDay, endDay)
				#two months
				elif (endMonth - startMonth) == 1:
					getMonth(dateRange, year, startMonth, True, False, startDay, endDay)
					getMonth(dateRange, year, endMonth, False, True, startDay, endDay)
				#more than two months
				else:
					getMonth(dateRange, year, startMonth, True, False, startDay, endDay)
					for month in range(endMonth - startMonth - 1):
						getMonth(dateRange, year, month + startMonth + 1, False, False, startDay, endDay)
					getMonth(dateRange, year, endMonth, False, True, startDay, endDay)
			#start month partial, end month full
			elif partialStartMonth == True and partialEndMonth == False:
				#first month
				getMonth(dateRange, year, startMonth, True, False, startDay, endDay)
				for month in range(endMonth - startMonth + 1):
					#additional months
					getMonth(dateRange, year, month + startMonth + 1, False, False, startDay, endDay)
			#start month full, end month partial
			elif partialStartMonth == False and partialEndMonth == True:
				for month in range(endMonth - startMonth):
					#initial months
					getMonth(dateRange, year, month + startMonth, False, False, startDay, endDay)
				#end month
				getMonth(dateRange, year, endMonth, False, True, startDay, endDay)
			#start month full, end month full
			elif partialStartMonth == False and partialEndMonth == False:
				for month in range(endMonth - startMonth + 1):
					getMonth(dateRange, year, month + startMonth, False, False, startDay, endDay)
		#start year but not end year
		elif year == startYear and not year == endYear:
			#start month partial
			if partialStartMonth == True:
				getMonth(dateRange, year, startMonth, True, False, startDay, endDay)
				for month in range(12 - startMonth):
					getMonth(dateRange, year, startMonth + month + 1, False, False, startDay, endDay)
			#start month full
			elif partialStartMonth == False:
				for month in range(13 - startMonth):
					getMonth(dateRange, year, startMonth + month, False, False, startDay, endDay)
		#not start year but end year
		elif not year == startYear and year == endYear:
			#end month partial
			if partialEndMonth == True:
				for month in range(endMonth - 1):
					getMonth(dateRange, year, month + 1, False, False, startDay, endDay)
				getMonth(dateRange, year, endMonth, False, True, startDay, endDay)
			#end month full
			elif partialEndMonth == False:
				for month in range(endMonth):
					getMonth(dateRange, year, month + 1, False, False, startDay, endDay)
		#not start or end year
		elif not year == startYear and not year == endYear:
			for month in range(12):
				getMonth(dateRange, year, month + 1, False, False, startDay, endDay)
	
	#return completed list
	return dateRange
	
def getMonth(dateRange, year, month, partialStart, partialEnd, startDay, endDay):
	if partialStart == True and partialEnd == False:
		for day in range(getDaysInMonth(month, getLeap(year)) - startDay + 1):
			dateRange.append([year, month, startDay + day])
	elif partialStart == False and partialEnd == True:
		for day in range(endDay):
			dateRange.append([year, month, day + 1])
	elif partialStart == True and partialEnd == True:
		for day in range(endDay - startDay + 1):
			dateRange.append([year, month, startDay + day])
	else:
		for day in range(getDaysInMonth(month, getLeap(year))):
			dateRange.append([year, month, day + 1])
	
def getDaysInMonth(month, leap):
	if	month	==	1:
		return 31
	elif	month	==	2 and leap == True:
		return 29
	elif	month	==	2 and leap == False:
		return 28
	elif	month	==	3:
		return 31
	elif	month	==	4:
		return 30
	elif	month	==	5:
		return 31
	elif	month	==	6:
		return 30
	elif	month	==	7:
		return 31
	elif	month	==	8:
		return 31
	elif	month	==	9:
		return 30
	elif	month	==	10:
		return 31
	elif	month	==	11:
		return 30
	elif	month	==	12:
		return 31
	
def getLeap(year):
	leap = True
	if year % 4 != 0:
		leap = False
	return leap
	
def getPartialStartMonth(month, day):
	partialMonth = False
	if day != 1:
		partialMonth = True
	return partialMonth
	
def getPartialEndMonth(month, day, leap):
	partialMonth = False
	if day < getDaysInMonth(month, leap):
		partialMonth = True
	return partialMonth