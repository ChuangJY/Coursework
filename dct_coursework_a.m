close all
clc

%part a
%Read lena.mat in and extract its size
load("Lena.mat");

%extract the 8 by 8 pixel region of image randomly
ebe = Lena(216:223, 216:223)

%perform the dct and inverse dct
dctt = dct2(ebe);
figure()
bar3(dctt)

%perform the inverse 2-D DCT Operation
%display it and comment it in report
invdct = idct2(dctt)

%part b
%read in the quantization matrix
load("M.mat");

%for research purpose, I also create a matrix for 10% quality factor
MM = [80 60 50 80 120 200 255 255;
      55 60 70 95 130 255 255 255;
      70 65 80 120 200 255 255 255;
      70 85 110 145 255 255 255 255;
      90 110 185 255 255 255 255 255;
      120 175 255 255 255 255 255 255;
      245 255 255 255 255 255 255 255;
      255 255 255 255 255 255 255 255;]

%Quantize the DCT coefficient using M matrix
%dividing the matrix of DCT matrix by M
buffer = dctt./M;

%rounding the result to the nearest integer
buffer = round(buffer);

%multiply the M to "undo" the quantization
buffer = buffer.*M;
figure()
bar3(buffer);

%Perform inverse DCT
%print the output and comment the result in report
ebe
invdct = idct2(buffer)

%Part C
%repeat part B, but perform on evey 8 by 8 pixels in Lena.mat
% Q50
fun = @dct2;
J = blkproc(Lena, [8 8], fun);
fun = @(J)J./M;
J = blkproc(J, [8 8], fun);
fun = @(J)round(J);
J = blkproc(J, [8 8], fun);
percentageZero50 = sum(J(:)==0)/(512*512);
fun = @(J)J.*M;
J = blkproc(J, [8 8], fun);
fun = @idct2;
J = blkproc(J, [8 8], fun);
ssim50 = ssim(Lena, J);
corelation50 = corr2(Lena, J);
MSE50 = immse(Lena, J);
figure(3)
imshow(uint8(J))
imwrite(uint8(J), 'compress50.png');
imwrite(uint8(J), 'compress50.jpg');
imwrite(uint8(J), 'compress50.tif');
figure(4)
imshow(uint8(Lena))
imwrite(uint8(Lena), 'uncompress.png');
imwrite(uint8(Lena), 'uncompress.jpg');
imwrite(uint8(Lena), 'uncompress.tif');

%Q10
fun = @dct2;
J = blkproc(Lena, [8 8], fun);
fun = @(J)J./MM;
J = blkproc(J, [8 8], fun);
fun = @(J)round(J);
J = blkproc(J, [8 8], fun);
percentageZero10 = sum(J(:)==0)/(512*512);
fun = @(J)J.*MM;
J = blkproc(J, [8 8], fun);
fun = @idct2;
J = blkproc(J, [8 8], fun);
ssim10 = ssim(Lena, J);
corelation10 = corr2(Lena, J);
MSE10 = immse(Lena, J);
figure(5)
imshow(uint8(J))
imwrite(uint8(J), 'compress10.png');
imwrite(uint8(J), 'compress10.jpg');
imwrite(uint8(J), 'compress10.tif');