Name

    SUN_geometry_compression_format


Name Strings

    GL_SUN_geometry_compression_format


Contact

    Jack Middleton, Sun (Jack.Middleton 'at' eng.sun.com)
    Mark Hood, Sun (Mark.Hood 'at' eng.sun.com)


Status

    Incomplete.


Version

    @(#)compressed_geometry_sun_format.spec 1.7 00/06/05


Number

    ???


Dependencies

    SUN_geometry_compression
    SUN_global_alpha


Overview

    This specification depends upon the SUN_geometry_compression extension and
    describes how Sun's compressed geometry format is used with that extension.
    The format itself is not fully described here, but in a separate document,
    the Compressed Geometry Specification by Michael F. Deering.


New Procedures and Functions

    void CompressedGeometryAttributesSUN(int wordOffset, sizei wordCount,
                                         float *attributes)

    void FinishCompressedGeometrySUN(ubyte *data)

    const ubyte *CompressedGeometryFormatVersionSUN(enum format) 


New Tokens

    Accepted by the <format> parameters of CompressedGeometrySUN and
    BeginCompressedGeometrySUN:

        COMPRESSED_GEOMETRY_LEVEL1_SUN             0x860A
        COMPRESSED_GEOMETRY_LEVEL2_SUN             0x860B        

    Additional flag bits accepted by the <geometryComponents> parameter of
    CompressedGeometrySUN:

        COMPRESSED_ALPHA_VALUES_SUN                0x10
        COMPRESSED_2ND_COLORS_SUN                  0x20

    Flag bits accepted by the <renderFlags> parameter of CompressedGeometrySUN:

        COMPRESSED_GEOMETRY_ASYNC_SUN              0x01

    Accepted by the <value> parameter of GetIntegerv, GetBooleanv, GetFloatv,
    and GetDoublev:

        NUM_COMPRESSED_GEOMETRY_DEVICE_FORMATS_SUN 0x860C
        COMPRESSED_GEOMETRY_DEVICE_FORMATS_SUN     0x860D
        COMPRESSED_GEOMETRY_MAX_ATTR_SIZE_SUN      0x860E
        COMPRESSED_GEOMETRY_CUR_ATTR_SIZE_SUN      0x860F
        COMPRESSED_GEOMETRY_ATTR_DATA_SUN          0x8610

    Accepted by the <target> parameter of Hint and the <value> parameter of
    GetIntegerv, GetBooleanv, GetFloatv, and GetDoublev:

        COMPRESSED_GEOMETRY_MESH_HINT_SUN          0x8611
        COMPRESSED_GEOMETRY_QUALITY_HINT_SUN       0x8612
        COMPRESSED_GEOMETRY_ENCODE_HINT_SUN        0x8613


Additions to Chapter 2 of the GL Specification (GL Operation)

    <Add the following text to section 2.14.1 "Rendering Compressed Geometry",
     in the discussion of the CompressedGeometrySUN command.>

    The <geometryType> parameter must indicate geometry of a consistent
    dimensionality when using the COMPRESSED_GEOMETRY_LEVEL1_SUN format
    version, either points, lines, or surfaces.  COMPRESSED_GEOMETRY_LEVEL2_SUN
    accepts any combination of geometry types.

    For the COMPRESSED_GEOMETRY_LEVEL1_SUN format version, the
    <geometryComponents> parameter is limited to COMPRESSED_NORMALS_SUN,
    COMPRESSED_COLORS_RGB_SUN, and COMPRESSED_COLORS_RGBA_SUN.

    COMPRESSED_GEOMETRY_LEVEL2_SUN allows COMPRESSED_TEXTURE_COORDS_SUN,
    COMPRESSED_ALPHAS_SUN, and COMPRESSED_2ND_COLORS_SUN to be specified in the
    <geometryComponents> parameter.  COMPRESSED_TEXTURE_COORDS_SUN indicates
    that texture coordinates are bundled with some or all of the vertices in
    the compressed object; these are limited to 4 2D texture coordinates or 2
    4D coordinates.  COMPRESSED_ALPHAS_SUN indicates that global alpha values
    are present.  COMPRESSED_2ND_COLORS_SUN indicates that some or all vertices
    have a secondary color bundled in addition to the primary color; if
    lighting is enabled, then the secondary color is mapped to the material
    specular color.

    The COMPRESSED_GEOMETRY_LEVEL2_SUN format also allows the
    COMPRESSED_GEOMETRY_ASYNC_SUN flag to be specified in the <renderFlags>
    parameter.  By default CompressedGeometrySUN does not return until the
    object has been rendered, but if this flag is set then the command is
    allowed to return immediately, if possible, so that the GL thread can
    continue with other tasks.  If this flag is set then the command
    FinishCompressedGeometrySUN described below must be called before any
    subsequent modification to the data.


    <Add the following subsections to 2.14.1, "Rendering Compressed Geometry">

    2.14.1.1 Compressed Geometry Device Formats

    The token NUM_COMPRESSED_GEOMETRY_DEVICE_FORMATS_SUN can be passed to the
    various GL query commands in order to determine how many compressed
    geometry formats, if any, are directly supported at the rendering device
    level.  They may be enumerated with COMPRESSED_GEOMETRY_DEVICE_FORMATS_SUN.
    If a format is directly supported by the rendering device, then its
    decompression and rendering is not performed by the GL renderer but by the
    device itself.


    2.14.1.2 Asynchronously Rendering Compressed Geometry

    If the COMPRESSED_GEOMETRY_LEVEL2_SUN format is directly supported at the
    rendering device level, then it is capable of being rendered asynchronously
    from the GL application thread.  If this mode is used then the command

        void FinishCompressedGeometrySUN(ubyte *data)

    must be called before the application modifies compressed data which may
    still be rendering.  It will block the GL execution thread until the
    compressed geometry to which the <data> parameter refers has completed
    rendering.  It is only effective with direct contexts in immediate mode
    and if the data was rendered with the COMPRESSED_GEOMETRY_ASYNC_SUN flag.
    There is no effect if asynchronous rendering is not supported on the
    target platform or if the format is not directly supported at the device
    level. 


    2.14.1.3  Parameterizing Compressed Geometry

    The COMPRESSED_GEOMETRY_LEVEL2_SUN format may contain indirect attributes
    that reference values in a separate block of data.  The command

        void CompressedGeometryAttributesSUN(int wordOffset, sizei wordCount,
                                             float *attributes)

    specifies that data, which is considered to be server state.  The indirect
    attributes state contains an implementation specific number of contiguous
    32-bit floating-point data words which may be queried by using the token
    COMPRESSED_GEOMETRY_MAX_ATTR_SIZE_SUN.  The initial values are undefined;
    attempts to access undefined values from indirect attribute instructions in
    a compressed object will result in undefined behavior.

    The <wordCount> parameter specifies the number of 32-bit floats to be
    copied into the indirect attributes state from the array specified by the
    <attributes> parameter.  The <wordOffset> parameter specifies that the
    attributes are to be copied into a contiguous block starting at the
    specified number of floats from the first indirect attributes location.
    The sum of <wordOffset> and <wordCount> must not be greater than the value
    returned by COMPRESSED_GEOMETRY_MAX_ATTR_SIZE_SUN.

    The SUN_geometry_compression_format extension does not describe the
    contents of the data contained in the indirect attributes state; its
    contents are defined by the compressor used to encode the geometry.  This
    extension does not provide any facility for generating compressed geometry
    objects that reference indirect attributes.  Typically these attributes
    contain data such as materials and transform matrices and allow
    applications to parameterize the rendering of the compressed data generated
    by external compressors.

    For example, if the indirect attributes state needs 8 RGBA colors, then an
    application would use this command with a <wordOffset> of 0, <wordCount>
    32, and pass an array of floats containing the 8 colors.  If then the
    application wanted to replace the third color, it would set <wordOffset>
    to 8, <wordCount> to 4, and pass an array of four floats representing the
    new RGBA color.

    There is only one set of compressed geometry attributes defined at any one
    time.  In immediate mode, any compressed geometry object that contains
    indirect attribute instructions will use the state of the attributes
    defined at the time the rendering command is executed.  If compiled into a
    display list, then the binding of attributes depends upon the setting of
    the COMPRESSED_DISPLAY_LISTS_SUN capability: if enabled, then the
    compressed geometry is compiled into the display list without being
    decompressed, and the attributes are bound at execution time; otherwise,
    the object is decompressed and the resulting commands compiled into the
    display list, with attributes binding at compilation time. 

    The following additional tokens are supported for queries:

        COMPRESSED_GEOMETRY_CUR_ATTR_SIZE_SUN

    returns the number of defined 32-bit floats in the indirect attributes
    state.  This is initially zero, indicating that none have been set.  It
    increases to the maximum of the sums of the <wordOffset> and <wordCount>
    parameters from all the CompressedGeometryAttributesSUN commands processed
    in the current context.

        COMPRESSED_GEOMETRY_ATTR_DATA_SUN

    returns the data contained in the compressed geometry attributes block.
    The calling routine must allocate enough space to hold all the data
    expected.


    <In the discussion of BeginCompressedGeometrySUN in section 2.14.2, add the
     following text.>

    The COMPRESSED_GEOMETRY_LEVEL1_SUN format can compress the following GL
    commands: Begin, End, Vertex, Normal, and Color.  For Vertex, only the
    Vertex2 and Vertex3 variants are supported; explicit W components are not
    allowed and are always assumed to be 1.0.

    The COMPRESSED_GEOMETRY_LEVEL2_SUN format version can compress the above
    plus TexCoord, ArrayElement, and DrawArrays.  In addition, the GL state
    commands Material, MultMatrix, PushMatrix, PopMatrix, Rotate, Scale, and
    Translate may also be compressed.

    Matrix commands operate on the model view matrix only (equivalent to
    calling MatrixMode with MODELVIEW_MATRIX).  Only uniform scale matrices
    without projection components are valid; INVALID_OPERATION will be set
    otherwise.  

    Sun compressed geometry formats are additionally described by a version
    number.  The query command

        const ubyte *CompressedGeometryFormatVersionSUN(enum format)

    returns a version number in a null-terminated string which indicates the
    version of the format to which GL commands will be compressed.  This number
    takes the form "major_number.minor_number.subminor_number".  It is provided
    as potentially useful information and is not otherwise used by this
    extension.


    <In the discussion of CompressedVertexQualitySun in section 2.14.2.1, add
     the following text.>

    For the Sun formats this value specifies the number of bits of quantization
    to apply to each positional XYZ component.  A value of 1.0 maps to 16 bits
    while a value of 0.0 maps to 1 bit.


    <In the discussion of CompressedColorQualitySun in section 2.14.2.1, add
     the following text.>

    For the Sun formats this value specifies the number of bits of quantization
    to apply to each color RGBA component.  A value of 1.0 maps to 16 bits,
    while a value of 0.0 maps to 1 bit.


    <In the discussion of CompressedNormalQualitySun in section 2.14.2.1, add
     the following text.>

    For the Sun formats this value specifies the number of bits of quantization
    to apply to each normal UV component.  A value of 1.0 maps to 6 bits while
    a value of 0.0 maps to 0 bits.  Quantized normals are represented by 3-bit
    octant/sextant pairs along with U and V, resulting in a total number of
    bits ranging from 6 to 18.


    <In the discussion of CompressedTextureCoordQualitySun in section 2.14.2.1,
     add the following text.>

    For the Sun formats this value specifies the number of bits of quantization
    to apply to each texture coordinate.  A value of 1.0 maps to 16 bits while
    a value of 0.0 maps to 1 bit.


Additions to Chapter 3 of the GL Specification (Rasterization)

    None


Additions to Chapter 4 of the GL Specification (Per-Fragment Operations
and the Framebuffer)

    None


Additions to Chapter 5 of the GL Specification (Special Functions)

    <modify Hints discussion in 5.6>

    ...FOG_HINT, indicating whether fog calculations are done per pixel or per
    vertex; and if the SUN_geometry_compression_format extension is available,
    COMPRESSED_GEOMETRY_ENCODE_HINT_SUN, COMPRESSED_GEOMETRY_QUALITY_HINT_SUN,
    and COMPRESSED_GEOMETRY_MESH_HINT_SUN, indicating desired compression
    efficiency tradeoffs described below.  <hint> must be one of FASTEST,
    indicating the most efficient option...

    The COMPRESSED_GEOMETRY_ENCODE_HINT_SUN value of FASTEST causes the
    extension to use a single-pass encoding algorithm that uses generic Huffman
    tables.  NICEST may invoke a two-pass encoding which performs a statistical
    analysis of data lengths in order to generate optimized Huffman tables.

    The COMPRESSED_GEOMETRY_QUALITY_HINT_SUN value of FASTEST indicates that
    the compression quality parameters specified by CompressedVertexQualitySUN,
    CompressedNormalQualitySUN, CompressedColorQualitySUN, and
    CompressedTextureCoordQualitySUN should be strictly followed.  NICEST means
    that the implementation might perform an analysis of the geometry
    complexity to determine if lower quality values are appropriate.

    If COMPRESSED_GEOMETRY_MESH_HINT_SUN is set to NICEST, then this indicates
    the application is providing geometry that may benefit from a topological
    analysis that finds vertices that can be shared between polygons and
    reordered into strips or meshes before compression.  FASTEST means the
    application doesn't need or desire a reordering of the vertices in its
    geometry.

    Values of DONT_CARE for these hints always default to FASTEST.


Additions to Chapter 6 of the GL Specification (State and State Requests)

    None


Additions to the GLX / WGL / AGL Specifications

    None


GLX Protocol

    CompressedGeometryAttributesSUN
      2             8 + 4 + byteCount    rendering command length
      2             16400                rendering command opcode
      4             CARD32               byteCount + 4
      4             CARD32               attribute word offset
      byteCount     CARD32               floating-point attribute data


Errors

    INVALID_VALUE raised by CompressedGeometryAttributesSUN if the sum of
    the <wordOffset> and <wordCount> parameters is greater than the attributes
    state size supported.

    Undefined results, including no rendering or abnormal program termination,
    if undefined indirect attributes are referenced by the compressed data
    passed to CompressedGeometrySUN.
    

New State

    Get Value                                 Get Command  Type  Initial Value
    ---------                                 -----------  ----  -------------
    COMPRESSED_GEOMETRY_MAX_ATTR_SIZE_SUN     GetIntegerv  Z     512
    COMPRESSED_GEOMETRY_CUR_ATTR_SIZE_SUN     GetIntegerv  Z     0            
    COMPRESSED_GEOMETRY_ATTR_DATA_SUN         GetFloatv    n x R undefined    
    COMPRESSED_GEOMETRY_MESH_HINT_SUN         GetIntegerv  Z     DONT_CARE    
    COMPRESSED_GEOMETRY_QUALITY_HINT_SUN      GetIntegerv  Z     DONT_CARE    
    COMPRESSED_GEOMETRY_ENCODE_HINT_SUN       GetIntegerv  Z     DONT_CARE    


New Implementation Dependent State

    none

