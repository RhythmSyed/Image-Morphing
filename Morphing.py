import numpy as np
import scipy
import imageio
import os
from PIL import Image, ImageDraw

from scipy.spatial import Delaunay
from scipy import interpolate

class Affine:

    def __init__(self, source, destination):

        if not source.dtype == np.float64 or not destination.dtype == np.float64:
            raise ValueError('input source or destination does not have type float64!')

        self.source = source
        self.destination = destination

        sourceMatrix = np.array([[source[0][0], source[0][1], 1, 0, 0, 0],
                                 [0, 0, 0, source[0][0], source[0][1], 1],
                                 [source[1][0], source[1][1], 1, 0, 0, 0],
                                 [0, 0, 0, source[1][0], source[1][1], 1],
                                 [source[2][0], source[2][1], 1, 0, 0, 0],
                                 [0, 0, 0, source[2][0], source[2][1], 1]])

        destinationMatrix = np.array([[destination[0][0]],
                                      [destination[0][1]],
                                      [destination[1][0]],
                                      [destination[1][1]],
                                      [destination[2][0]],
                                      [destination[2][1]]])

        h = np.linalg.solve(sourceMatrix, destinationMatrix)

        matrix = np.matrix([[h[0][0], h[1][0], h[2][0]],
                            [h[3][0], h[4][0], h[5][0]],
                            [0, 0, 1]])

        self.matrix = np.linalg.inv(matrix)

    def transform(self, sourceImage, destinationImage):
        if not isinstance(sourceImage, np.ndarray) or not isinstance(destinationImage, np.ndarray):
            raise TypeError('sourceImage or destinationImage is not a numpy array')

        mask = Image.new('L', (len(sourceImage[0]), len(sourceImage)), 0)
        ImageDraw.Draw(mask).polygon([(self.destination[0][0], self.destination[0][1]), (self.destination[1][0], self.destination[1][1]), (self.destination[2][0], self.destination[2][1])], outline=255, fill=255)
        mask = np.array(mask)

        rectangle = interpolate.RectBivariateSpline(range(len(sourceImage)), range(len(sourceImage[0])), sourceImage, kx=1, ky=1)
        mask = np.transpose(np.nonzero(mask))

        for y,x in mask:
            targetMatrix = np.matrix([[x],
                                      [y],
                                      [1]])

            outputMatrix = np.matmul(self.matrix, targetMatrix)
            destinationImage[y][x] = rectangle.ev(outputMatrix[1][0], outputMatrix[0][0])

class Blender:

    def __init__(self, startImage, startPoints, endImage, endPoints):
        if not isinstance(startImage, np.ndarray) or not isinstance(startPoints, np.ndarray) or not isinstance(endImage, np.ndarray) or not isinstance(endPoints, np.ndarray):
            raise TypeError('startImage, startPoints, endImage, or endPoints are not a numpy array')

        self.startImage = startImage
        self.startPoints = startPoints
        self.endImage = endImage
        self.endPoints = endPoints

        self.delaunayTriangles = Delaunay(startPoints).simplices


    def getBlendedImage(self, alpha):
        midTriangle = np.zeros(shape=(3,2), dtype=np.float64)
        startingTriangle = np.zeros(shape=(3,2), dtype=np.float64)
        endingTriangle = np.zeros(shape=(3,2), dtype=np.float64)

        imageFromSource = np.zeros(shape=(len(self.startImage), len(self.startImage[0])), dtype=np.uint8)
        imageFromEnd = np.zeros(shape=(len(self.startImage), len(self.startImage[0])), dtype=np.uint8)
        morphed = np.zeros(shape=(len(self.startImage), len(self.startImage[0])), dtype=np.uint8)

        for i in range(len(self.delaunayTriangles)):
            for j in range(len(self.delaunayTriangles[i])):
                index = self.delaunayTriangles[i][j]
                startX = self.startPoints[index][0]
                startY = self.startPoints[index][1]
                endX = self.endPoints[index][0]
                endY = self.endPoints[index][1]

                xMidTri = ((1 - alpha) * startX) + (alpha * endX)
                yMidTri = ((1 - alpha) * startY) + (alpha * endY)
                midCoorList = (xMidTri, yMidTri)
                midTriangle[j] = midCoorList

                startCoorList = (startX, startY)
                startingTriangle[j] = startCoorList

                endCoorList = (endX, endY)
                endingTriangle[j] = endCoorList

            startToMid = Affine(startingTriangle, midTriangle)
            startToMid.transform(self.startImage, imageFromSource)

            endToMid = Affine(endingTriangle, midTriangle)
            endToMid.transform(self.endImage, imageFromEnd)

        morphed = (((1 - alpha) * imageFromSource) + (alpha * imageFromEnd)).astype(np.uint8)

        return morphed

    def generateMorphVideo(self, targetFolderPath, sequenceLength, includeReversed):
        increment = 1 / sequenceLength
        imageNum = 1
        alpha = 0
        if includeReversed == False:
            while not alpha > 1:
                myImage = self.getBlendedImage(alpha)
                imageio.imwrite(targetFolderPath + '/frame{:03d}.jpg', format(imageNum), myImage)
                alpha = alpha + increment
                imageNum += 1
        elif includeReversed == True:
            while not alpha > 1:
                myImage = self.getBlendedImage(alpha)
                imageio.imwrite(targetFolderPath + '/frame{:03d}.jpg', format(imageNum), myImage)
                alpha = alpha + increment
                imageNum += 1
            alpha = 1
            while not alpha < 0:
                myImage = self.getBlendedImage(alpha)
                imageio.imwrite(targetFolderPath + '/frame{:03d}.jpg', format(imageNum), myImage)
                alpha = alpha - increment
                imageNum += 1

        os.system("ffmpeg -r 5 -i frame{:03d}.jpg -vcodec mpeg4 -y morph.mp4")





class ColorAffine:

    def __init__(self, source, destination):

        if not source.dtype == np.float64 or not destination.dtype == np.float64:
            raise ValueError('input source or destination does not have type float64!')

        self.source = source
        self.destination = destination

        sourceMatrix = np.array([[source[0][0], source[0][1], 1, 0, 0, 0],
                                 [0, 0, 0, source[0][0], source[0][1], 1],
                                 [source[1][0], source[1][1], 1, 0, 0, 0],
                                 [0, 0, 0, source[1][0], source[1][1], 1],
                                 [source[2][0], source[2][1], 1, 0, 0, 0],
                                 [0, 0, 0, source[2][0], source[2][1], 1]])

        destinationMatrix = np.array([[destination[0][0]],
                                      [destination[0][1]],
                                      [destination[1][0]],
                                      [destination[1][1]],
                                      [destination[2][0]],
                                      [destination[2][1]]])

        h = np.linalg.solve(sourceMatrix, destinationMatrix)

        matrix = np.matrix([[h[0][0], h[1][0], h[2][0]],
                            [h[3][0], h[4][0], h[5][0]],
                            [0, 0, 1]])

        self.matrix = np.linalg.inv(matrix)

    def transform(self, sourceImage, destinationImage):
        if not isinstance(sourceImage, np.ndarray) or not isinstance(destinationImage, np.ndarray):
            raise TypeError('sourceImage or destinationImage is not a numpy array')

        mask = Image.new('L', (len(sourceImage[0]), len(sourceImage)), 0)
        ImageDraw.Draw(mask).polygon([(self.destination[0][0], self.destination[0][1]), (self.destination[1][0], self.destination[1][1]), (self.destination[2][0], self.destination[2][1])], outline=255, fill=255)
        mask = np.array(mask)
        mask = np.transpose(np.nonzero(mask))

        sourceImagenew = np.transpose(sourceImage)

        R = interpolate.RectBivariateSpline(range(len(sourceImagenew[0])), range(len(sourceImagenew[0][0])), sourceImagenew[0], kx=1, ky=1)
        G = interpolate.RectBivariateSpline(range(len(sourceImagenew[1])), range(len(sourceImagenew[1][0])), sourceImagenew[1], kx=1, ky=1)
        B = interpolate.RectBivariateSpline(range(len(sourceImagenew[2])), range(len(sourceImagenew[2][0])), sourceImagenew[2], kx=1, ky=1)

        for y,x in mask:
            targetMatrix = np.matrix([[x],
                                      [y],
                                      [1]])

            outputMatrix = np.matmul(self.matrix, targetMatrix)
            for z in range(len(sourceImage[0][2])):
                if z == 0:
                    destinationImage[y][x][z] = R.ev(outputMatrix[0][0], outputMatrix[1][0])
                if z == 1:
                    destinationImage[y][x][z] = G.ev(outputMatrix[0][0], outputMatrix[1][0])
                if z == 2:
                    destinationImage[y][x][z] = B.ev(outputMatrix[0][0], outputMatrix[1][0])

class ColorBlender:

    def __init__(self, startImage, startPoints, endImage, endPoints):
        if not isinstance(startImage, np.ndarray) or not isinstance(startPoints, np.ndarray) or not isinstance(endImage, np.ndarray) or not isinstance(endPoints, np.ndarray):
            raise TypeError('startImage, startPoints, endImage, or endPoints are not a numpy array')

        self.startImage = startImage
        self.startPoints = startPoints
        self.endImage = endImage
        self.endPoints = endPoints


        self.delaunayTriangles = Delaunay(startPoints).simplices


    def getBlendedImage(self, alpha):
        midTriangle = np.zeros(shape=(3,2), dtype=np.float64)
        startingTriangle = np.zeros(shape=(3,2), dtype=np.float64)
        endingTriangle = np.zeros(shape=(3,2), dtype=np.float64)

        imageFromSource = np.zeros(shape=(len(self.startImage), len(self.startImage[0]), len(self.startImage[0][0])), dtype=np.uint8)
        imageFromEnd = np.zeros(shape=(len(self.startImage), len(self.startImage[0]), len(self.startImage[0][0])), dtype=np.uint8)
        morphed = np.zeros(shape=(len(self.startImage), len(self.startImage[0]), len(self.startImage[0][0])), dtype=np.uint8)

        for i in range(len(self.delaunayTriangles)):
            for j in range(len(self.delaunayTriangles[i])):
                index = self.delaunayTriangles[i][j]
                startX = self.startPoints[index][0]
                startY = self.startPoints[index][1]
                endX = self.endPoints[index][0]
                endY = self.endPoints[index][1]

                xMidTri = ((1 - alpha) * startX) + (alpha * endX)
                yMidTri = ((1 - alpha) * startY) + (alpha * endY)
                midCoorList = (xMidTri, yMidTri)
                midTriangle[j] = midCoorList

                startCoorList = (startX, startY)
                startingTriangle[j] = startCoorList

                endCoorList = (endX, endY)
                endingTriangle[j] = endCoorList

            startToMid = ColorAffine(startingTriangle, midTriangle)
            startToMid.transform(self.startImage, imageFromSource)

            endToMid = ColorAffine(endingTriangle, midTriangle)
            endToMid.transform(self.endImage, imageFromEnd)

        morphed = (((1 - alpha) * imageFromSource) + (alpha * imageFromEnd)).astype(np.uint8)

        return morphed

if __name__ == "__main__":
    startImage = imageio.imread('WolfGray.jpg')
    startPoints = np.loadtxt('wolf.jpg.txt', usecols=range(2), dtype=np.float64)
    endPoints = np.loadtxt('tiger2.jpg.txt', usecols=range(2), dtype=np.float64)
    endImage = imageio.imread('Tiger2Gray.jpg')

    blenderInstance = Blender(startImage, startPoints, endImage, endPoints)
    myImage = blenderInstance.getBlendedImage(0.5)

    #blenderInstance.generateMorphVideo('video', 8, False)
    imageio.imwrite('finaltest.png', myImage)


    #givenImage = np.array(imageio.imread('frame021.png'))
    #print(np.mean(np.abs(givenImage-myImage)))
