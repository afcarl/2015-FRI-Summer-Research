#   This is a code that converts an obj file into a piece of javascript code
# that generates a model of a tree. Below is an implementation for the purpsose,
# written in MATLAB.
#
# clear all; close all; clc;
#
# data = importdata('bust2.obj');
# vertices = data.data(1:36259, :);
# faces = data.data(36260:end, :);
#
# fid = fopen('code_for_Colonel.txt','w');
# for i=1:length(faces)
#     face_vertices = zeros(1,9);
#     start = 1;
#     stop = 3;
#     for j=1:3
#         face_vertices(start:stop) = vertices(faces(i,j), :);
#         start = stop+1;
#         stop = start+2;
#     end
#     fprintf(fid,'mesh.triangle([%f, %f, %f], [%f, %f, %f],
#                   [%f, %f, %f]);\n', face_vertices);
# end
# fclose(fid);
#
# PYTHON IMPLEMENTATION
F_PATH = "./t.obj"      # file path
obj = open(F_PATH, "r") # read the obj file
