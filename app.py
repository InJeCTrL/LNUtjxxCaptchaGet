import requests
import cv2
import os

class LNUtjxxCaptchaGet: 
    def __init__(self):
        ''' import number samples, binarize images, and save to a list
        '''
        self.__sample_number = []
        for i in range(10):
            src_img = cv2.imread("./samples/%d.png" % i, 0)
            ret, result_img = cv2.threshold(src_img, 127, 255, cv2.THRESH_BINARY)
            self.__sample_number.append(result_img)
    def getCode(self, path_img):
        ''' get text of the captcha
        path_img:           captcha image file path
        return:             [captcha text content, original captcha image]
        '''
        retcode = ""
        checkcode_ori = cv2.imread(path_img, 0)
        ret, checkcode = cv2.threshold(checkcode_ori, 127, 255, cv2.THRESH_BINARY)
        for i in range(4):
            # cut captcha picture
            n = checkcode[0:10, 2 + i * 10:2 + i * 10 + 6]
            for i_sample, sample in enumerate(self.__sample_number):
                right = True
                # verify if each ZERO position in sample covered the cutted captcha
                for pt in range(60):
                    if sample[pt % 10][pt // 10] == 0 and sample[pt % 10][pt // 10] != n[pt % 10][pt // 10]:
                        right = False
                        break
                if right:
                    retcode += str(i_sample)
        return [retcode, checkcode_ori]
                    
if __name__ == "__main__":
    # download real captcha from "tjxx.lnu.edu.cn"
    url_checkcode = "http://tjxx.lnu.edu.cn/inc/checkcode.asp"
    with requests.get(url_checkcode) as response:
        with open("tmp.png", "wb") as f:
            f.write(response.content)

    bp = LNUtjxxCaptchaGet()
    code, checkcode = bp.getCode("tmp.png")
    print(code)
    
    # clear temp checkcode downloaded
    os.remove("./tmp.png")

    # show captcha image
    cv2.imshow("checkcode", checkcode)
    cv2.waitKey(0)
