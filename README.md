# geometry-compression
Java 3D implementation of Michael F. Deering's geometry compression specification

In 2002 at Sun Microsystems I was involved in a few aspects of Java 3D, including implementing geometry compression.
Michael F. Deering did the seminal work in this field, publishing research into quantizing positions, textures, and
a novel normal compression technique. A Huffman encoding of these compressed geometry elements provided perceptually 
lossless 5:1 compression ratios.  This was particularly important in an era when geometric models were commonly 
distributed on CD-ROM media, RAM was expensive, and bandwith across the CPU and GPU system busses was a 
performance bottleneck.

Michael's work resulted in a hardware implementation of the geometry decompressor (the Sun Elite3D GPU) along with 
high performance C code to encode geometry into the compressed geometry format.  This was incorporated into Sun's
version of OpenGL and was submitted as a potential OpenGL extension to the ARB (I worked on these specifications and 
they are included in this archive).

In addition, I implemented the geometry compression specification in Java 3D based on the original C implementation and
the specification included as Appendix B of the Java 3D specification.  The work was never properly optimized but still 
provided significant performance advantages even with software decompression. This work is archived here.
