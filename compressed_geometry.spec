Name

    SUN_geometry_compression


Name Strings

    GL_SUN_geometry_compression


Contact

    Jack Middleton, Sun (Jack.Middleton 'at' eng.sun.com)
    Mark Hood, Sun (Mark.Hood 'at' eng.sun.com)


Status

    Incomplete.


Version

    @(#)compressed_geometry.spec 1.25 00/06/05


Number

    ???


Dependencies

    None.


Overview

    Compressed geometry can reduce memory usage, file space, and transmission
    times, and on some platforms can increase rendering performance.  This
    specification does not define a format to represent such compressed
    geometry, but instead provides the framework for rendering and creating
    compressed geometry objects in a format-neutral fashion, allowing
    applications to query the GL for supported formats and to choose which of
    those to use for subsequent rendering and compression purposes.  Specific
    compressed geometry formats are defined by other extensions which are
    dependent on the framework provided here for the actual rendering and
    compression functions.

    A new command, CompressedGeometrySUN, is provided to render compressed
    geometry objects, and two mechanisms are provided to compress geometric
    data.  The first and simplest compression facility simply directs the GL to
    compress display lists whenever possible, by enabling the GL capability
    switch COMPRESSED_DISPLAY_LISTS_SUN; the other allows applications to
    explictly create compressed geometry objects using Begin/End semantics and
    GL primitive commands.

    The latter mechanism creates objects that, unlike display lists, contain
    data that can be stored, rendered with CompressedGeometrySUN, and
    otherwise manipulated.  This is performed by calling the command
    BeginCompressedGeometrySUN, issuing the desired GL commands to be
    compressed, and then retrieving the compressed data with a call to
    EndCompressedGeometrySUN.  In this mode specific compressed geometry
    formats may impose a number of restrictions on the commands that can be
    issued in order to successfully create the object.

    New tokens are defined for use with the various GL query commands to allow
    applications to determine what compressed geometry formats are supported
    by the extension implementation.


New Procedures and Functions

    void CompressedGeometrySUN(enum format, uint geometryType,
                               uint geometryComponents, uint renderFlags,
                               sizei size, ubyte *data)

    void BeginCompressedGeometrySUN(enum format)
    ubyte *EndCompressedGeometrySUN(sizei *size,
                                    uint *geometryType,
                                    uint *geometryComponents,
                                    float *scale, float *originX,
                                    float *originY, float *originZ)

    void CompressedVertexQualitySUN(float quality)
    void CompressedNormalQualitySUN(float quality)
    void CompressedColorQualitySUN(float quality)
    void CompressedTextureCoordQualitySUN(float quality)


New Tokens

    Accepted by the <format> parameter of CompressedGeometrySUN and
    BeginCompressedGeometrySUN:

        <tokens defined by dependent extensions>

    Flag bits accepted by the <geometryType> parameter of CompressedGeometrySUN:

        COMPRESSED_POINTS_SUN                     0x01
        COMPRESSED_LINES_SUN                      0x02
        COMPRESSED_SURFACES_SUN                   0x04

    Flag bits accepted by the <geometryComponents> parameter of
    CompressedGeometrySUN:

        COMPRESSED_NORMALS_SUN                    0x01
        COMPRESSED_COLORS_RGB_SUN                 0x02
        COMPRESSED_COLORS_RGBA_SUN                0x04
        COMPRESSED_TEXTURE_COORDS_SUN             0x08

    Flag bits accepted by the <renderFlags> parameter of CompressedGeometrySUN:

        <flags defined by dependent extensions>

    Accepted by the <value> parameter of GetIntegerv, GetBooleanv, GetFloatv,
    and GetDoublev:

        NUM_COMPRESSED_GEOMETRY_FORMATS_SUN       0x8600
        COMPRESSED_GEOMETRY_FORMATS_SUN           0x8601
        COMPRESSED_VERTEX_QUALITY_SUN             0x8602
        COMPRESSED_NORMAL_QUALITY_SUN             0x8603
        COMPRESSED_COLOR_QUALITY_SUN              0x8604
        COMPRESSED_TEXTURE_COORD_QUALITY_SUN      0x8605

    Accepted by the <cap> parameter of Enable:

        COMPRESSED_DISPLAY_LISTS_SUN              0x8606


Additions to Chapter 2 of the GL Specification (GL Operation)

    2.14 Compressed Geometry

    Graphics primitives with their associated positions, colors, normals,
    texture coordinates, and other data may be compressed and rendered through
    the GL via commands provided by the SUN_geometry_compression extension.
    If this extension is present the string "GL_SUN_geometry_compression" will
    be returned with the set of strings returned by GetString(EXTENSIONS).

    This specification does not define specific compressed geometry formats.
    Tokens are defined for use with the various GL query commands to allow
    applications to determine what compressed geometry formats defined by other
    dependent specifications are supported by the extension implementation.
    NUM_COMPRESSED_GEOMETRY_FORMATS_SUN provides the number of compressed
    geometry formats supported, while COMPRESSED_GEOMETRY_FORMATS_SUN returns
    an array of that number of tokens enumerating all the specific formats
    supported.


    2.14.1 Rendering Compressed Geometry

    The command

        void CompressedGeometrySUN(enum format, uint geometryType,
                                   uint geometryComponents, uint renderFlags,
                                   sizei size, ubyte *data)

    either renders compressed geometry immediately or adds it to a display
    list.  If the command is called between a NewList/EndList pair, then
    whether or not the object is decompressed before compiling it into a
    display list depends upon the setting of the COMPRESSED_DISPLAY_LISTS_SUN
    capability: if enabled, then the compressed geometry is always added to the
    display list as is; otherwise, the renderer may choose to decompress the
    object and compile the resulting commands into the display list instead.

    The <format> parameter indicates the specific format into which the
    geometry has been compressed.  If the GL renderer is incompatible then
    INVALID_ENUM will be raised.

    The <geometryType> parameter indicates the dimensionality of the geometry
    present in the compressed data, specified with the following flag bit
    values:

        COMPRESSED_POINTS_SUN
        COMPRESSED_LINES_SUN
        COMPRESSED_SURFACES_SUN

    This parameter provides the renderer with information about the geometric
    connectivity encoded into the compressed object before having to decompress
    it, and is not necessarily used or needed by every renderer for each
    supported compressed geometry format.  Some formats described by other
    dependent specifications may also impose restrictions on mixing geometry of
    different dimensionality into the same object.

    The <geometryComponents> parameter indicates what geometric components are
    present in addition to the required vertex coordinates, specified with the
    following bit values:

        COMPRESSED_NORMALS_SUN
        COMPRESSED_COLORS_RGB_SUN
        COMPRESSED_COLORS_RGBA_SUN
        COMPRESSED_TEXTURE_COORDS_SUN

    As with the <geometryType>, this parameter provides information to the
    renderer before having to decompress it, and may or may not be used or
    required by a specific format or implementation; some formats may impose
    limitations on what types of components are allowed, or perhaps define
    additional components.  The interpretation of each flag bit value defined
    above is as follows:

    If COMPRESSED_NORMALS_SUN is specified, then the compressed geometry
    contains normals, either as standalone normal instructions or bundled with
    vertices or both, and is suitable for lighting.  These instructions have
    the same semantics as GL Normal commands.

    If COMPRESSED_COLORS_RGB_SUN is specified, then the compressed geometry
    contains RGB colors, either as standalone color instructions or bundled
    with vertices or both.  These instructions have the semantics of Color3
    commands, either specifying primary vertex colors directly if no lighting
    is applied, or setting the properties specified by ColorMaterial if
    COLOR_MATERIAL is enabled.

    COMPRESSED_COLORS_RGBA_SUN indicates that the compressed geometry contains
    RGBA colors with alpha values, either as standalone color instructions or
    bundled with vertices or both.  These instructions have the semantics of
    Color4 commands.

    COMPRESSED_TEXTURE_COORDS_SUN indicates that texture coordinates are
    bundled with some or all of the vertices in the compressed object.  Some
    formats may impose limitations on the number of dimensions allowed, and
    whether or not multiple textures may be mapped to a vertex.

    The flag bits for the <renderFlags> parameter are defined by formats
    described in separate dependent specifications.  This parameter may or may
    not be used or required by a specific format, and is intended to provide
    additional information potentially useful in rendering the compressed
    geometry.

    The <data> parameter points to the beginning of a block of compressed
    geometry in the format specified.  The length of the data in bytes is given
    by the <size> parameter.

    If any of the parameters above other than <format> are not compatible with
    the renderer, then the command is ignored and INVALID_VALUE raised.
    If the data itself is invalid then the results are undefined.

    GL state is inherited and can be modified by the compressed geometry object
    as it is rendered.  This includes state such as the current matrix and
    material properties, as well as vertex state such as color, normal, and
    texture coordinates.  The resulting value of these attributes in the GL
    context after rendering compressed geometry is undefined.

    When geometry is compressed its vertex positions may be scaled and
    translated into a normalized quantization space.  To place the compressed
    geometry back to its original position in the scene a scale and offset
    value may need to be appended to the model-view matrix.  For example:

        Translatef(xo, yo, zo);
        Scalef(scale, scale, scale);
        CompressedGeometrySUN(ver, type, flags, size, data);

    When the GL computes the inverse transpose of the model-view matrix (needed
    to transform the normals), it does not rescale the normals.  This will
    result in incorrect lighting, so enabling the RESCALE_NORMAL attribute is
    required.


    2.14.2 Compressing GL Commands

    A subset of GL commands may be compressed into an object that can be
    rendered with CompressedGeometrySUN.  The command

        void BeginCompressedGeometrySUN(enum format)

    initiates the building of a compressed geometry object.  Subsequent Begin
    and End pairs are used to define the geometry to be compressed.  If the
    given format is not supported then INVALID_ENUM is raised and the geometry
    is ignored.  Compression of GL commands in this manner is always a
    client-side operation.

    The primitive commands that are always allowed when building compressed
    geometry objects are Begin, End, Vertex, and Normal.  Specific compressed
    geometry formats defined in other specifications may allow other primitive
    commands such as Color, TexCoord, ArrayElement, and DrawArrays, in
    addition to GL state commands such as Material, MultMatrix, PushMatrix,
    and PopMatrix.  If a command is not supported by the given format or the
    extension itself, then it is ignored and INVALID_OPERATION is raised.

    To terminate the building of compressed geometry object and return the
    results, the command

        ubyte *EndCompressedGeometrySUN(sizei *size,
                                        uint *geometryType,
                                        uint *geometryComponents,
                                        float *scale, float *originX,
                                        float *originY, float *originZ)

    is used.  If there are no errors while compressing, a pointer to a buffer
    of the length <size> containing the compressed geometry will be returned as
    the value of the command.  The caller is responsible for freeing this
    memory.  

    The <geometryType> and <geometryComponents> parameters are filled in with
    information as described in the CompressedGeometrySUN command.

    Compressed data may be scaled and translated into a normalized space.  The
    <scale>, <originX>, <originY>, and <originZ> parameters are filled in with
    the values needed to return the data to its original position and size,
    through, e.g., the following calls:

        Translatef(originX, originY, originZ);
        Scalef(scale, scale, scale);
        CompressedGeometrySUN(format, type, components, flags, size, data);

    GL state is not affected by any commands invoked between a call to
    BeginCompressedGeometrySUN and EndCompressedGeometrySUN.  These commands
    are always executed immediately and are not compiled into display lists.


    2.14.2.1 Quality Parameters

    Part of the compression process may involve decreasing the quality or
    precision of floating-point vertex components in order to approximate them
    with representations of shorter bit length.  The following four commands
    set minimum quality values for the compression of all subsequent vertex
    component data.

    The values are normalized to the range [0.0 - 1.0], with 0.0 indicating the
    worst approximation and 1.0 indicating the best approximation; 1.0 is
    always the default.  Values outside these ranges are clamped.

        void CompressedVertexQualitySUN(float quality)

    specifies the minimum quality to be used for approximating subsequent XYZ
    position components.

        void CompressedColorQualitySUN(float quality)

    specifies the minimum quality to be used for approximating subsequent
    color and alpha components.

        void CompressedNormalQualitySUN(float quality)

    specifies the minimum quality to be used for approximating subsequent
    normal components.

        void CompressedTextureCoordQualitySUN(float quality)

    specifies the minimum quality to be used for approximating subsequent
    texture coordinate components.

    These commands are always executed immediately and are not compiled into
    display lists.

    The query commands accept the following tokens to return the above values:

        COMPRESSED_VERTEX_QUALITY_SUN
        COMPRESSED_NORMAL_QUALITY_SUN
        COMPRESSED_COLOR_QUALITY_SUN
        COMPRESSED_TEXTURE_COORD_QUALITY_SUN

     

Additions to Chapter 3 of the GL Specification (Rasterization)

    None


Additions to Chapter 4 of the GL Specification (Per-Fragment Operations
and the Framebuffer)

    None


Additions to Chapter 5 of the GL Specification (Special Functions)

    5.4 Display Lists

    <add to the list of commands which are not compiled into display lists>

    BeginCompressedGeometrySUN, EndCompressedGeometrySUN,
    CompressedVertexQualitySUN, CompressedNormalQualitySUN,
    CompressedColorQualitySUN, CompressedTextureCoordQualitySUN.


    <add to the end of the display list discussion in 5.4>

    If the SUN_geometry_compression extension is available, then display lists
    may be compressed into an opaque implementation-defined format. This is
    done by calling Enable with the token COMPRESSED_DISPLAY_LISTS_SUN to
    indicate that subsequently defined display lists should be compressed
    whenever possible, until the Disable command is called with the same
    token.  The CompressedGeometrySUN rendering command is not used in this
    mode.

    There are no restrictions on the GL commands that may be placed in
    compressed display lists aside from the normal restrictions on
    uncompressed display lists. When commands are encountered that cannot be
    compressed GL may break up the display list into smaller segments that can
    themselves be compressed, or choose to abandon compression entirely.

    If the SUN_geometry_compression is available but the value of
    NUM_COMPRESSED_GEOMETRY_FORMATS_SUN is 0, then display list compression is
    the only provided means of compressing geometry and rendering it.


Additions to Chapter 6 of the GL Specification (State and State Requests)

    None


Additions to the GLX / WGL / AGL Specifications

    None


GLX Protocol

    A compressed geometry rendering command is sent to the server as part of
    either a variable-length GLXRender request or a series of variable-length
    GLXRenderLarge requests.

    GLXRender:

        CompressedGeometrySUN
          2             8 + 16 + byteCount   rendering command length
          2             16399                rendering command opcode
          4             CARD32               byteCount + 16
          4             CARD32               format specifier
          4             CARD32               geometry type
          4             CARD32               geometry components
          4             CARD32               render flags
          byteCount     CARD8                compressed data

    GLXRenderLarge:

        CompressedGeometrySUN
          4             12 + 16 + byteCount  rendering command length
          4             16399                rendering command opcode
          4             CARD32               byteCount + 16
          4             CARD32               format specifier
          4             CARD32               geometry type
          4             CARD32               geometry components
          4             CARD32               render flags
          byteCount     CARD8                compressed data

    The format specifier word indicates which of the formats supported by the
    implementation was used to encode the subsequent compressed data.

    The valid bit values for the geometry type word are:

          0x01    compressed points
          0x02    compressed lines
          0x04    compressed surfaces

    The bit values defined by this specification for the geometry components
    word are:

          0x01    compressed normals
          0x02    compressed RGB colors
          0x04    compressed RGBA colors
          0x08    compressed texture coordinates

    Valid bit values for the render flags word are defined by dependent
    extensions. 

    Geometry compression commands that affect GL state are sent to the server
    in the following fixed-length GLXRender requests:

        CompressedVertexQualitySUN
          2             4 + 4                rendering command length
          2             16401                rendering command opcode
          4             CARD32               position quality

        CompressedNormalQualitySUN
          2             4 + 4                rendering command length
          2             16402                rendering command opcode
          4             CARD32               normal quality

        CompressedColorQualitySUN
          2             4 + 4                rendering command length
          2             16403                rendering command opcode
          4             CARD32               color quality

        CompressedTextureCoordQualitySUN
          2             4 + 4                rendering command length
          2             16404                rendering command opcode
          4             CARD32               texture quality


Errors

    INVALID_ENUM raised by CompressedGeometrySUN and BeginCompressedGeometrySUN
    if an unsupported compressed geometry format is specified.

    INVALID_VALUE raised by CompressedGeometrySUN if the <geometryType>,
    <geometryComponents>, or <renderFlags> parameters contain unsupported
    values.

    INVALID_OPERATION raised by unsupported GL commands issued between
    BeginCompressedGeometrySUN and EndCompressedGeometrySUN.

    Undefined results, including no rendering or abnormal program termination,
    if invalid compressed data is passed to CompressedGeometrySUN.


New State

    Get Value                                 Get Command  Type  Initial Value
    ---------                                 -----------  ----  -------------
    COMPRESSED_VERTEX_QUALITY_SUN             GetFloatv    R     1.0          
    COMPRESSED_NORMAL_QUALITY_SUN             GetFloatv    R     1.0          
    COMPRESSED_COLOR_QUALITY_SUN              GetFloatv    R     1.0          
    COMPRESSED_TEXTURE_COORD_QUALITY_SUN      GetFloatv    R     1.0          
    COMPRESSED_DISPLAY_LISTS_SUN              IsEnabled    B     False        


New Implementation Dependent State

    Get Value                                 Get Command  Type
    ---------                                 -----------  ----
    NUM_COMPRESSED_GEOMETRY_FORMATS_SUN       GetIntegerv  Z   
    COMPRESSED_GEOMETRY_FORMATS_SUN           GetIntegerv  n x Z

    Get Value                                 Value   
    ---------                                 -----
    NUM_COMPRESSED_GEOMETRY_FORMATS_SUN       number of formats 
    COMPRESSED_GEOMETRY_FORMATS_SUN           formats supported
