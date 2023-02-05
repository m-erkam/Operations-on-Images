
# return img, nested list
def read_ppm_file(f):
    fp = open(f)
    fp.readline()  # reads P3 (assume it is P3 file)
    lst = fp.read().split()
    n = 0
    n_cols = int(lst[n])
    n += 1
    n_rows = int(lst[n])
    n += 1
    max_color_value = int(lst[n])
    n += 1
    img = []
    for r in range(n_rows):
        img_row = []
        for c in range(n_cols):
            pixel_col = []
            for i in range(3):
                pixel_col.append(int(lst[n]))
                n += 1
            img_row.append(pixel_col)
        img.append(img_row)
    fp.close()
    return img, max_color_value


# Works
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


filename = input()
operation = int(input())


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE


def operation_1(f):
    # I take max and min inputs from the user
    minimum = int(input())
    maximum = int(input())
    # I create list of pixels correspond to the whole image
    img = read_ppm_file(f)[0]
    max_color_value = read_ppm_file(f)[1]
    for i in range(len(img)):
        for j in range(len(img[i])):
            for k in range(len(img[i][j])):
                # I apply min max normalization for every channel value
                a = (img[i][j][k]/max_color_value) * (maximum - minimum) + minimum
                a = round(a, 4)
                # Then I change previous list with new channel values
                img[i][j][k] = a
    # Printing changed image using provided printer function
    img_printer(img)


def operation_2(f):
    # First I assign sum variables for every channel value to calculate mean
    sum_red = 0
    sum_green = 0
    sum_blue = 0
    # Then I assign second sum variables to use while calculating standard deviation
    sum_red_2 = 0
    sum_green_2 = 0
    sum_blue_2 = 0
    img = read_ppm_file(f)[0]
    for i in range(len(img)):
        for j in range(len(img[i])):
            for k in range(len(img[i][j])):
                # I calculate sum values for every channel
                if k == 0:
                    sum_red += img[i][j][k]
                if k == 1:
                    sum_green += img[i][j][k]
                if k == 2:
                    sum_blue += img[i][j][k]

    # Using sum values, I calculate mean values
    mean_red = sum_red / (len(img) * len(img[0]))
    mean_green = sum_green / (len(img) * len(img[0]))
    mean_blue = sum_blue / (len(img) * len(img[0]))

    for i in range(len(img)):
        for j in range(len(img[i])):
            for k in range(len(img[i][j])):
                # I calculate the sum which is in the standard deviation formula
                if k == 0:
                    sum_red_2 += (img[i][j][k] - mean_red) ** 2
                if k == 1:
                    sum_green_2 += (img[i][j][k] - mean_green) ** 2
                if k == 2:
                    sum_blue_2 += (img[i][j][k] - mean_blue) ** 2
    # Using second sum values, I calculate standard deviation for every channel
    standard_dev_red = ((sum_red_2 / (len(img) * len(img[0]))) ** 0.5) + 1e-6
    standard_dev_green = ((sum_green_2 / (len(img) * len(img[0]))) ** 0.5) + 1e-6
    standard_dev_blue = ((sum_blue_2 / (len(img) * len(img[0]))) ** 0.5) + 1e-6

    for i in range(len(img)):
        for j in range(len(img[i])):
            for k in range(len(img[i][j])):
                # I apply z-score normalization formula for channels
                # And I change old values with news
                if k == 0:
                    z_score_normal_red = round((img[i][j][k] - mean_red) / standard_dev_red, 4)
                    img[i][j][k] = z_score_normal_red
                if k == 1:
                    z_score_normal_green = round((img[i][j][k] - mean_green) / standard_dev_green, 4)
                    img[i][j][k] = z_score_normal_green
                if k == 2:
                    z_score_normal_blue = round((img[i][j][k] - mean_blue) / standard_dev_blue, 4)
                    img[i][j][k] = z_score_normal_blue
    # Printing changed image using provided printer function
    img_printer(img)


def operation_3(f):
    img = read_ppm_file(f)[0]
    for i in range(len(img)):
        for j in range(len(img[i])):
            # For each pixel, I calculate average value
            avr = int(sum(img[i][j])/3)
            for k in range(len(img[i][j])):
                # And I change every channel value with average value
                img[i][j][k] = avr
    # I print all pixel values
    img_printer(img)


def operation_4(f):
    img = read_ppm_file(f)[0]
    max_color_value = read_ppm_file(f)[1]
    # I define a list to store the filter
    whole_filter = []
    # I take filter name from the user
    fh = open(input()).read().split()
    stride = int(input())
    fh1 = len(fh)
    # Then I add each value of filter to the list
    for i in range(int(fh1 ** 0.5)):
        filter_1 = []
        for j in range(int(fh1 ** 0.5)):
            filter_1.append(float(fh[0]))
            fh.remove(fh[0])
        whole_filter.append(filter_1)
    # I create variables for each channel to store the summation values after apply filter to the channel values
    sum_0 = 0
    sum_1 = 0
    sum_2 = 0
    # I define a list to store new values of each pixel
    filtered = []
    # And I define another list to add the new pixel and to create new image
    filtered_pic = []
    # I use for loops to access each channel value which should be applied the filter
    for i in range((len(img)-(int(fh1 ** 0.5)-1))//stride):
        for j in range((len(img[0])-(int(fh1 ** 0.5)-1))//stride):
            # The program applies filter according to filter's length
            for col in range(int(fh1 ** 0.5)):
                for length in range(int(fh1 ** 0.5)):
                    sum_0 += (img[stride*i + col][stride*j + length][0] * whole_filter[col][length])
                    sum_1 += (img[stride*i + col][stride*j + length][1] * whole_filter[col][length])
                    sum_2 += (img[stride*i + col][stride*j + length][2] * whole_filter[col][length])
            # When new value is less than 0 I set it 0
            # And is greater than max color value I set it max color value
            if sum_0 < 0:
                sum_0 = 0
            if sum_0 > max_color_value:
                sum_0 = max_color_value
            if sum_1 < 0:
                sum_1 = 0
            if sum_1 > max_color_value:
                sum_1 = max_color_value
            if sum_2 < 0:
                sum_2 = 0
            if sum_2 > max_color_value:
                sum_2 = max_color_value
            # I add new pixel with new channel values to the new list
            filtered.append([int(sum_0), int(sum_1), int(sum_2)])
            # I reset the sum values before new calculations
            sum_0 = 0
            sum_1 = 0
            sum_2 = 0
        # I add rows to another new list
        filtered_pic.append(filtered)
        # And I reset the row list
        filtered = []
    # The program prints all pixels
    img_printer(filtered_pic)


def operation_5(f):
    img = read_ppm_file(f)[0]
    max_color_value = read_ppm_file(f)[1]
    # I define a list to store the filter
    whole_filter = []
    # I take filter name from the user
    fh = open(input()).read().split()
    stride = int(input())
    fh1 = len(fh)
    # Then I add each value of filter to the list
    for i in range(int(fh1 ** 0.5)):
        filter_1 = []
        for j in range(int(fh1 ** 0.5)):
            filter_1.append(float(fh[0]))
            fh.remove(fh[0])
        whole_filter.append(filter_1)
    # Here, I add 0 values to the picture like a frame according to filter's size
    n = (int(fh1 ** 0.5) - 1) // 2
    for width in range(n):
        img.insert(0, [[0, 0, 0]]*len(img[0]))
        img.insert(len(img), [[0, 0, 0]]*len(img[0]))
        for i in range(len(img[0])+2):
            img[i].insert(0, [0, 0, 0])
            img[i].insert(len(img[0]), [0, 0, 0])
    # Then I apply operation 4 to the new image
    # I create variables for each channel to store the summation values after apply filter to the channel values
    sum_0 = 0
    sum_1 = 0
    sum_2 = 0
    # I define a list to store new values of each pixel
    filtered = []
    # And I define another list to add the new pixel and to create new image
    filtered_pic = []
    # I use for loops to access each channel value which should be applied the filter
    for i in range((len(img) - (int(fh1 ** 0.5) - 1)) // stride):
        for j in range((len(img) - (int(fh1 ** 0.5) - 1)) // stride):
            # The program applies filter according to filter's length
            for col in range(int(fh1 ** 0.5)):
                for length in range(int(fh1 ** 0.5)):
                    sum_0 += (img[stride * i + col][stride * j + length][0] * whole_filter[col][length])
                    sum_1 += (img[stride * i + col][stride * j + length][1] * whole_filter[col][length])
                    sum_2 += (img[stride * i + col][stride * j + length][2] * whole_filter[col][length])
            # When new value is less than 0 I set it 0
            # And is greater than max color value I set it max color value
            if sum_0 < 0:
                sum_0 = 0
            if sum_0 > max_color_value:
                sum_0 = max_color_value
            if sum_1 < 0:
                sum_1 = 0
            if sum_1 > max_color_value:
                sum_1 = max_color_value
            if sum_2 < 0:
                sum_2 = 0
            if sum_2 > max_color_value:
                sum_2 = max_color_value
            # I add new pixel with new channel values to the new list
            filtered.append([int(sum_0), int(sum_1), int(sum_2)])
            # I reset the sum values before new calculations
            sum_0 = 0
            sum_1 = 0
            sum_2 = 0
            # I add rows to another new list
        filtered_pic.append(filtered)
        # And I reset the row list
        filtered = []
        # The program prints all pixels
    img_printer(filtered_pic)


def operation_6(f, img, pixel_range, c=0, r=0):
    # When a column is completed applying quantization on the first row and column number is odd, the program goes
    # r+1 th column (r is column, c is row)
    # And if the column number exceeds length of image it prints whole image pixels
    if c == 0 and r % 2 == 1:
        try:
            # These lines check r th and r+1 th column's values
            # If these are between range the program change second value with first value
            if -pixel_range < int(img[c][r][0]) - int(img[c][r+1][0]) < pixel_range:
                if -pixel_range < int(img[c][r][1]) - int(img[c][r+1][1]) < pixel_range:
                    if -pixel_range < int(img[c][r][2]) - int(img[c][r+1][2]) < pixel_range:
                        img[c][r+1] = img[c][r]
            # The program goes r+1 th column via recursive call
            return operation_6(f, img, pixel_range, c, r + 1)
        except:
            return img_printer(img)

    # When a column is completed applying quantization on the last row and row number is even, the program goes
    # r+1 th column
    # And if the column number exceeds length of image it prints whole image pixels
    if c == len(img[0]) - 1 and r % 2 == 0:
        try:
            # These lines check r th and r+1 th column's values
            # If these are between range the program change second value with first value
            if -pixel_range < int(img[c][r][0]) - int(img[c][r+1][0]) < pixel_range:
                if -pixel_range < int(img[c][r][1]) - int(img[c][r+1][1]) < pixel_range:
                    if -pixel_range < int(img[c][r][2]) - int(img[c][r+1][2]) < pixel_range:
                        img[c][r+1] = img[c][r]
            # The program goes r+1 th column via recursive call
            return operation_6(f, img, pixel_range, c, r + 1)
        except:
            return img_printer(img)

    # (If column number is even) The program compare c th and c+1 th rows channel values and if their difference is
    # less than range it changes second value to the first value
    if r % 2 == 0:
        if -pixel_range < int(img[c][r][0]) - int(img[c + 1][r][0]) < pixel_range:
            if -pixel_range < int(img[c][r][1]) - int(img[c + 1][r][1]) < pixel_range:
                if -pixel_range < int(img[c][r][2]) - int(img[c + 1][r][2]) < pixel_range:
                    img[c + 1][r] = img[c][r]

    # (If column number is odd) The program compare c th and c+1 th rows channel values and if their difference is
    # less than range it changes second value to the first value
    if r % 2 == 1:
        if -pixel_range < int(img[c][r][0]) - int(img[c-1][r][0]) < pixel_range:
            if -pixel_range < int(img[c][r][1]) - int(img[c-1][r][1]) < pixel_range:
                if -pixel_range < int(img[c][r][2]) - int(img[c-1][r][2]) < pixel_range:
                    img[c-1][r] = img[c][r]

    # When a comparison is done, the program decide whether go up or down according to column number
    if r % 2 == 0:
        operation_6(f, img, pixel_range, c + 1, r)
    if r % 2 == 1:
        operation_6(f, img, pixel_range, c - 1, r)


def operation_7(f, img, pixel_range, c=0, r=0, ch=0):
    # When a channel value (for example all reds) is completed, program goes ch+1th channel and compare ch th and
    # ch+1 th values then starts checking it upward or downward
    # Two base conditions because red and blue values finish on the first row and green values finish on the last row
    if len(img) % 2 == 0:
        if c == 0 and r == len(img[0]) - 1:
            if ch % 3 == 0:
                if -pixel_range < img[c][r][0] - img[c][r][1] < pixel_range:
                    img[c][r][1] = img[c][r][0]
                return operation_7(f, img, pixel_range, c, r, ch + 1)
            if ch % 3 == 2:
                return operation_7(f, img, pixel_range, c, r, ch + 1)
        if c == 0 and r == 0:
            if ch % 3 == 1:
                if -pixel_range < img[c][r][1] - img[c][r][2] < pixel_range:
                    img[c][r][2] = img[c][r][1]
                return operation_7(f, img, pixel_range, c, r, ch + 1)
    # Base condition for when image size is odd
    if len(img) % 2 == 1:
        if c == 0 and r == 0:
            if ch % 3 == 1:
                if -pixel_range < img[c][r][1] - img[c][r][2] < pixel_range:
                    img[c][r][2] = img[c][r][1]
                return operation_7(f, img, pixel_range, c, r, ch + 1)
        if c == len(img[0]) - 1 and r == len(img[0]) - 1:
            if ch % 3 == 0:
                if -pixel_range < img[c][r][0] - img[c][r][1] < pixel_range:
                    img[c][r][1] = img[c][r][0]
                return operation_7(f, img, pixel_range, c, r, ch + 1)
            if ch % 3 == 2:
                return operation_7(f, img, pixel_range, c, r, ch + 1)

    # When a column is completed applying quantization on the first row and column number is odd and if channel value
    # is 0 or 2, the program goes r+1 th column (r is column, c is row), if channel value is 1 the program goes r-1 th
    # column
    # And if the column number exceeds length of image it prints pixels of whole image
    if c == 0:
        try:
            if ch % 3 == 0 or ch % 3 == 2:
                if r % 2 == 1:
                    if -pixel_range < int(img[c][r][ch % 3]) - int(img[c][r + 1][ch % 3]) < pixel_range:
                        img[c][r + 1][ch % 3] = img[c][r][ch % 3]
                    return operation_7(f, img, pixel_range, c, r + 1, ch)
            if ch % 3 == 1:
                if r % 2 == 0:
                    if -pixel_range < int(img[c][r][ch % 3]) - int(img[c][r - 1][ch % 3]) < pixel_range:
                        img[c][r - 1][ch % 3] = img[c][r][ch % 3]
                    return operation_7(f, img, pixel_range, c, r - 1, ch)
        except:
            return img_printer(img)

    # When a column is completed applying quantization on the last row and row number is even and if channel value is
    # 0 or 2, the program goes r+1 th column, if channel value is 1, the program goes r-1 th column
    # And if the column number exceeds length of image it prints pixels of whole image
    if c == len(img[0]) - 1:
        try:
            if ch % 3 == 0 or ch % 3 == 2:
                if r % 2 == 0:
                    if -pixel_range < int(img[c][r][ch % 3]) - int(img[c][r+1][ch % 3]) < pixel_range:
                        img[c][r + 1][ch % 3] = img[c][r][ch % 3]
                    return operation_7(f, img, pixel_range, c, r + 1, ch)
            if ch % 3 == 1:
                if r % 2 == 1:
                    if -pixel_range < int(img[c][r][ch % 3]) - int(img[c][r-1][ch % 3]) < pixel_range:
                        img[c][r - 1][ch % 3] = img[c][r][ch % 3]
                    return operation_7(f, img, pixel_range, c, r - 1, ch)
        except:
            return img_printer(img)

    # (If channel value is 0 or 2) The program compares c and c+1 th value if column value is even
    # And if column number is odd, it compares c and c-1 th values
    if ch % 3 == 0:
        if r % 2 == 0:
            if -pixel_range < int(img[c][r][0]) - int(img[c + 1][r][0]) < pixel_range:
                img[c + 1][r][0] = img[c][r][0]
        if r % 2 == 1:
            if -pixel_range < int(img[c][r][0]) - int(img[c - 1][r][0]) < pixel_range:
                img[c - 1][r][0] = img[c][r][0]

    if ch % 3 == 2:
        if r % 2 == 0:
            if -pixel_range < int(img[c][r][2]) - int(img[c + 1][r][2]) < pixel_range:
                img[c + 1][r][2] = img[c][r][2]
        if r % 2 == 1:
            if -pixel_range < int(img[c][r][2]) - int(img[c - 1][r][2]) < pixel_range:
                img[c - 1][r][2] = img[c][r][2]

    # (If channel value is 1) Program compares c and c-1 th values of the row if column value is even
    # And if column number is odd it compares c and c+1 th values
    if ch % 3 == 1:
        if r % 2 == 0:
            if -pixel_range < int(img[c][r][1]) - int(img[c - 1][r][1]) < pixel_range:
                img[c - 1][r][1] = img[c][r][1]
        if r % 2 == 1:
            if -pixel_range < int(img[c][r][1]) - int(img[c + 1][r][1]) < pixel_range:
                img[c + 1][r][1] = img[c][r][1]

    # When a comparison is done, the program decide whether go up or down according to column number and channel value
    # If mod of channel value is 0 or 2 and column number is even it goes down
    # If mod of channel value is 0 or 2 and column number is odd it goes up
    if ch % 3 == 0 or ch % 3 == 2:
        if r % 2 == 0:
            operation_7(f, img, pixel_range, c + 1, r, ch)
        if r % 2 == 1:
            operation_7(f, img, pixel_range, c - 1, r, ch)

    # If mod of channel value is 1 and column number is even it goes up
    # If mod of channel value is 1 and column number is odd it goes down
    if ch % 3 == 1:
        if r % 2 == 0:
            operation_7(f, img, pixel_range, c - 1, r, ch)
        if r % 2 == 1:
            operation_7(f, img, pixel_range, c + 1, r, ch)


def printing(f, o):
    # The program apply operation according to given inputs
    if o == 1:
        return operation_1(f)
    if o == 2:
        return operation_2(f)
    if o == 3:
        return operation_3(f)
    if o == 4:
        return operation_4(f)
    if o == 5:
        return operation_5(f)
    # For operation 6 and 7 I take a range input from the user
    if o == 6:
        a = read_ppm_file(filename)[0]
        pixel_range = int(input())
        return operation_6(f, a, pixel_range)
    if o == 7:
        a = read_ppm_file(filename)[0]
        pixel_range = int(input())
        return operation_7(f, a, pixel_range)


printing(filename, operation)

# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

