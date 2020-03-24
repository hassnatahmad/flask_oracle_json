CREATE TABLE A_GEOMETRIES
(
    "A_GEOMETRIES_ID" VARCHAR(50) NOT NULL,
    "CRD"             VARCHAR(50),
    "DG1"             VARCHAR(50),
    "DG2"             VARCHAR(50),
    "DG3"             VARCHAR(50),
    "EA1"             VARCHAR(50),
    "ED1"             VARCHAR(50),
    "EE3"             VARCHAR(50),
    "EF1"             VARCHAR(50),
    "EF2"             VARCHAR(50),
    "EF3"             VARCHAR(50),
    "EG1"             VARCHAR(50),
    "EG6"             VARCHAR(50),
    "EK1"             VARCHAR(50),
    "EK23"            VARCHAR(50),
    "EP1"             VARCHAR(50),
    "EP2"             VARCHAR(50),
    "ET21"            VARCHAR(50),
    "ET23"            VARCHAR(50),
    "ET25"            VARCHAR(50),
    "GC11"            VARCHAR(50),
    "GC13"            VARCHAR(50),
    "GD1"             VARCHAR(50),
    "GD2"             VARCHAR(50),
    "GD3"             VARCHAR(50),
    "GF1"             VARCHAR(50),
    "GF3"             VARCHAR(50),
    "GF4"             VARCHAR(50),
    "GF7"             VARCHAR(50),
    "GG1"             VARCHAR(50),
    "GG22"            VARCHAR(50),
    "GG3"             VARCHAR(50),
    "GK1"             VARCHAR(50),
    "GK10"            VARCHAR(50),
    "GK22"            VARCHAR(50),
    "GK24"            VARCHAR(50),
    "GS0"             VARCHAR(50),
    "GS1"             VARCHAR(50),
    "GS43"            VARCHAR(50),
    "GT1"             VARCHAR(50),
    "GT2"             VARCHAR(50),
    "GT3"             VARCHAR(50),
    "GT4"             VARCHAR(50),
    "PX1"             VARCHAR(50),
    "SE1"             VARCHAR(50),
    "SP1"             VARCHAR(50),
    "WC1"             VARCHAR(50),
    PRIMARY KEY ("A_GEOMETRIES_ID")
);
CREATE TABLE B_TESTS
(
    "B_TESTS_ID"          VARCHAR(50) NOT NULL,
    "Test ID"             VARCHAR(50),
    "Type"                VARCHAR(50),
    "Description"         VARCHAR(50),
    "CRD"                 VARCHAR(50),
    "Tag"                 VARCHAR(50),
    "Tire size"           VARCHAR(50),
    "Rim width (in)"      VARCHAR(50),
    "Rim contour"         VARCHAR(50),
    "Rim diameter (in)"   VARCHAR(50),
    "Construction number" VARCHAR(50),
    PRIMARY KEY ("B_TESTS_ID")
);

CREATE TABLE C_LOADING_CONDITIONS
(
    "C_LOADING_ID"                   VARCHAR(50) NOT NULL,
    "Test ID"                        VARCHAR(50),
    "Test-load-pressure ID"          VARCHAR(50),
    "Pressure (bar)"                 VARCHAR(50),
    "Vertical load (kg)"             VARCHAR(50),
    "SD (mm)"                        VARCHAR(50),
    "OD (mm)"                        VARCHAR(50),
    "CL (mm)"                        VARCHAR(50),
    "Width (mm)"                     VARCHAR(50),
    "ISL (mm)"                       VARCHAR(50),
    "OSL (mm)"                       VARCHAR(50),
    "Net area (mm2)"                 VARCHAR(50),
    "Gross area (mm2)"               VARCHAR(50),
    "FSF"                            VARCHAR(50),
    "DOF"                            VARCHAR(50),
/*"Vertical spring rate tangent (N/mm)" VARCHAR(50),*/
    "Vertical spring rate tangent (" VARCHAR(50),
/*"Vertical spring rate secant (N/mm)" VARCHAR(50),*/
    "Vertical spring rate secant (N" VARCHAR(50),
    "Lateral spring rate (N/mm)"     VARCHAR(50),
/*"Longitudinal spring rate (N/mm)" VARCHAR(50),*/
    "Longitudinal spring rate (N/mm" VARCHAR(50),
    "Torsional spring rate (N/mm)"   VARCHAR(50),
    "RRc"                            VARCHAR(50),
    "RR (kg)"                        VARCHAR(50),
    "Loss (N-mm/rev)"                VARCHAR(50),
    "Temperature (C)"                VARCHAR(50),
    "CS"                             VARCHAR(50),
    "SAS"                            VARCHAR(50),
    "TD"                             VARCHAR(50),
    "FP"                             VARCHAR(50),
    "SR"                             VARCHAR(50),
    "RR"                             VARCHAR(50),
    "FM"                             VARCHAR(50),
    PRIMARY KEY ("C_LOADING_ID")
);


CREATE TABLE D_COMPONENTS
(
    "D_COMPONENTS_ID"    VARCHAR(50) NOT NULL,
    "Test-component ID"             VARCHAR(50),
    "Test ID"                VARCHAR(50),
    "Component"         VARCHAR(50),
    "Compound"                 VARCHAR(50),
    "Volume (mm3)"                 VARCHAR(50),
    PRIMARY KEY ("D_COMPONENTS_ID")
);
CREATE TABLE E_COMPONENTS
(
    "E_COMPONENTS_ID"    VARCHAR(50) NOT NULL,
    "Test-load-pressure-component I"             VARCHAR(50),
    "Test-load-pressure ID"                VARCHAR(50),
    "Component"         VARCHAR(50),
    "Energy Diss. Per Rev. (N-mm)"                 VARCHAR(50),
    "Energy Diss. % of Total"                 VARCHAR(50),
    PRIMARY KEY ("E_COMPONENTS_ID")
);

CREATE TABLE A_GEOMETRIES_EXTRA
(
    "A_GEOMETRIES_EXTRA_ID" VARCHAR(50) NOT NULL,
    "A_GEOMETRIES_ID"       VARCHAR(50),
    "Column name"           VARCHAR(50),
    "Column value"          VARCHAR(50),
    PRIMARY KEY ("A_GEOMETRIES_EXTRA_ID"),
    CONSTRAINT FK_A_GEOMETRIES_ID FOREIGN KEY ("A_GEOMETRIES_ID")
        REFERENCES A_GEOMETRIES ("A_GEOMETRIES_ID")
);
CREATE TABLE B_TESTS_EXTRA
(
    "B_TESTS_EXTRA_ID" VARCHAR(50) NOT NULL,
    "B_TESTS_ID"       VARCHAR(50),
    "Column name"      VARCHAR(50),
    "Column value"     VARCHAR(50),
    PRIMARY KEY ("B_TESTS_EXTRA_ID"),
    CONSTRAINT FK_B_TEST_ID FOREIGN KEY ("B_TESTS_ID")
        REFERENCES B_TESTS ("B_TESTS_ID")
);
CREATE TABLE C_LOADING_EXTRA
(
    "C_LOADING_EXTRA_ID"    VARCHAR(50),
    "C_LOADING_ID"          VARCHAR(50),
    "Column name"           VARCHAR(50),
    "Column value"          VARCHAR(50),
    PRIMARY KEY ("C_LOADING_EXTRA_ID"),
    CONSTRAINT FK_C_LOADING_ID FOREIGN KEY ("C_LOADING_ID")
        REFERENCES C_LOADING_CONDITIONS ("C_LOADING_ID")
);
CREATE TABLE D_COMPONENTS_EXTRA
(
    "D_COMPONENTS_EXTRA_ID"    VARCHAR(50),
    "D_COMPONENTS_ID" VARCHAR(50),
    "Column name"           VARCHAR(50),
    "Column value"          VARCHAR(50),
    PRIMARY KEY ("D_COMPONENTS_EXTRA_ID"),
    CONSTRAINT FK_D_COMPONENTS_ID FOREIGN KEY ("D_COMPONENTS_ID")
        REFERENCES D_COMPONENTS ("D_COMPONENTS_ID")
);
CREATE TABLE E_COMPONENTS_EXTRA
(
    "E_COMPONENTS_EXTRA_ID"    VARCHAR(50),
    "E_COMPONENTS_ID"          VARCHAR(50),
    "Column name"           VARCHAR(50),
    "Column value"          VARCHAR(50),
    PRIMARY KEY ("E_COMPONENTS_EXTRA_ID"),
    CONSTRAINT FK_E_COMPONENTS_ID FOREIGN KEY ("E_COMPONENTS_ID")
        REFERENCES E_COMPONENTS ("E_COMPONENTS_ID")
);
CREATE TABLE A_B
(
    "A_B_ID"          VARCHAR2(50) NOT NULL,
    "B_TESTS_ID"      VARCHAR2(50),
    "A_GEOMETRIES_ID" VARCHAR2(50),
    PRIMARY KEY ("A_B_ID"),
    CONSTRAINT "FK_A_B_TESTS_ID" FOREIGN KEY ("B_TESTS_ID") REFERENCES B_TESTS ("B_TESTS_ID"),
    CONSTRAINT "FK_A_B_GEOMETRIES_ID" FOREIGN KEY ("A_GEOMETRIES_ID") REFERENCES A_GEOMETRIES ("A_GEOMETRIES_ID")
);

CREATE TABLE B_C
(
    "B_C_ID"       VARCHAR2(50) NOT NULL,
    "B_TESTS_ID"   VARCHAR2(50),
    "C_LOADING_ID" VARCHAR2(50),
    PRIMARY KEY ("B_C_ID"),
    CONSTRAINT "FK_B_C_TESTS_ID" FOREIGN KEY ("B_TESTS_ID") REFERENCES B_TESTS ("B_TESTS_ID"),
    CONSTRAINT "FK_B_C_LOADING_ID" FOREIGN KEY ("C_LOADING_ID") REFERENCES C_LOADING_CONDITIONS ("C_LOADING_ID")
);
CREATE TABLE B_D
(
    "B_D_ID"          VARCHAR2(50) NOT NULL,
    "B_TESTS_ID"      VARCHAR2(50),
    "D_COMPONENTS_ID" VARCHAR2(50),
    PRIMARY KEY ("B_D_ID"),
    CONSTRAINT "FK_B_D_TESTS_ID" FOREIGN KEY ("B_TESTS_ID") REFERENCES B_TESTS ("B_TESTS_ID"),
    CONSTRAINT "FK_B_D_COMPONENTS_ID" FOREIGN KEY ("D_COMPONENTS_ID") REFERENCES D_COMPONENTS ("D_COMPONENTS_ID")
);

CREATE TABLE C_E
(
    "C_E_ID"       VARCHAR2(50) NOT NULL,
    "C_LOADING_ID"   VARCHAR2(50),
    "E_COMPONENTS_ID" VARCHAR2(50),
    PRIMARY KEY ("C_E_ID"),
    CONSTRAINT "FK_C_E_LOADING_ID" FOREIGN KEY ("C_LOADING_ID") REFERENCES C_LOADING_CONDITIONS ("C_LOADING_ID"),
    CONSTRAINT "FK_C_E_COMPONENTS_ID" FOREIGN KEY ("E_COMPONENTS_ID") REFERENCES E_COMPONENTS ("E_COMPONENTS_ID")
);
