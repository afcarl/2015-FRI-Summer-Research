clear all; close all; clc;

data = importdata('bust2.obj');
vertices = data.data(1:36259, :);
faces = data.data(36260:end, :);

fid = fopen('code_for_Colonel.txt','w');
for i=1:length(faces)
    face_vertices = zeros(1,9);
    start = 1;
    stop = 3;
    for j=1:3
        face_vertices(start:stop) = vertices(faces(i,j), :);
        start = stop+1;
        stop = start+2;
    end
    fprintf(fid, 'mesh.triangle([ %f, %f, %f], [ %f, %f, %f], [ %f, %f, %f]);\n', face_vertices);
end
fclose(fid);
