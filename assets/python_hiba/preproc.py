def hiba_preproc(img):
    points = list(np.linspace(0, 1023, 16, dtype=np.int))
    img_bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Horizon Detect
    ys = []
    for p in points:
        col = img[:, p, 2]
        has_new = False
        for i in range(len(col)-1):
            if(float(col[i+1])-float(col[i]) < -45):  # arbitrary limit, seems fine
                ys.append(i)
                has_new = True
                break
        if(not has_new):
            ys.append(0)

    for i in range(len(ys)-1, 0, -1):
        if(ys[i] == 0):
            ys.pop(i)
            points.pop(i)

    # replace maximum with the avg of neighbours
    imax1 = 0  # indeces start at the top, so actually min
    imax2 = 0
    imax3 = 0
    for i in range(len(ys)):
        if(ys[imax3] >= ys[i]):
            imax3 = imax2
            imax2 = imax1
            imax1 = i

    # drop maxima
    drp = [imax1, imax2, imax3]
    drp.sort(reverse=True)
    for i in drp:
        ys.pop(i)
        points.pop(i)
    # fix the edges
    if(points.count(1023) == 0):
        points.append(1023)
        ys.append(ys[-1])
    if(points.count(0) == 0):
        points.insert(0, 0)
        ys.insert(0, ys[0])
    img_rgb = img.copy()
    for i in range(len(ys)-1):
        cv2.line(img_rgb, (points[i], ys[i]),(points[i+1], ys[i+1]), (255, 0, 0), 2)

    img_bw = cv2.erode(img_bw, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
    img_bw = cv2.GaussianBlur(img_bw, (13, 13), cv2.BORDER_DEFAULT)
    img_bw = cv2.adaptiveThreshold(img_bw, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    _,img_bw = cv2.threshold(img_bw, 127, 255, cv2.THRESH_BINARY) 
    img_bw = cv2.erode(img_bw, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
    img_bw = cv2.dilate(img_bw, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

    for i in range(len(ys)-1):
        for j in range(points[i], points[i+1]):
            y = int((ys[i]+ys[i+1])/2)-20
            col = img_bw[y:, j]
            for k in range(len(col)):
                col[k] = 255
                pass

    contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bbox = []
    for i in range(len(contours)):
        contours[i] = cv2.approxPolyDP(contours[i], 3, True)
        bbox.append(list(cv2.boundingRect(contours[i])))
        cv2.drawContours(img_rgb, contours, i, (0, 255, 0))

    # img_bw, contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # bbox=[]
    # print(img.shape[0]/2)
    # for i in range(len(contours)):
        # bb=cv2.boundingRect(contours[i])
        # if(len(contours[i]) > 8 and bb[1] < img.shape[0]/2): #drop too small objects
        # contours[i]=cv2.approxPolyDP(contours[i], 3, True)
        # bbox.append(list(bb))
    return img_rgb, bbox

    