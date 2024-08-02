# Verify Outputs from riverFeatures.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_verifyRiverFeatures -xv

# Pytests to Compare and Verify Expected Outputs
from io import StringIO

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width


def river_class_object():
    csv_example = StringIO()
    csv_example.write("llat,llon,rlat,rlon\n")
    csv_example.write(
        "30.03758064742554,-92.86856870164003,30.03744106431763,-92.867475846432\n"
    )
    csv_example.write(
        "30.03761289873068,-92.86854932864129,30.03744779451432,-92.86747357248917\n"
    )
    csv_example.write(
        "30.03764767910492,-92.86854615646305,30.03748158510661,-92.86744912321454\n"
    )
    csv_example.write(
        "30.03767440933011,-92.86853555132092,30.03750644719021,-92.86743200196584\n"
    )
    csv_example.write(
        "30.03770236278642,-92.8685329553435,30.03752454918347,-92.86743019872145\n"
    )
    csv_example.write(
        "30.03772919351539,-92.86852225012414,30.0375426005056,-92.8674152219088\n"
    )
    csv_example.write(
        "30.0377490549762,-92.86851215967346,30.0375721590616,-92.8674007572212\n"
    )
    csv_example.write(
        "30.03778301480612,-92.86850070336355,30.03760885519144,-92.86738399853574\n"
    )
    csv_example.write(
        "30.03781601910584,-92.86848128471483,30.03763647218977,-92.86736152540908\n"
    )
    csv_example.write(
        "30.03784317873953,-92.86847053431235,30.0376710739572,-92.86733658820407\n"
    )
    csv_example.write(
        "30.03787040125924,-92.8684597471607,30.03771036353054,-92.86730115646196\n"
    )
    csv_example.write(
        "30.03790600092315,-92.86845640697538,30.0377475921359,-92.86728394049267\n"
    )
    csv_example.write(
        "30.0379404991904,-92.86844485391589,30.03778027570281,-92.86726385834064\n"
    )
    csv_example.write(
        "30.03796197755238,-92.86844283088163,30.03779189842327,-92.86725099533921\n"
    )
    csv_example.write(
        "30.03801823414788,-92.86842918514924,30.03782231186275,-92.86723594951347\n"
    )
    csv_example.write(
        "30.03804707600122,-92.8684264587786,30.03785992478739,-92.86721837516968\n"
    )
    csv_example.write(
        "30.03807720971334,-92.86843197572428,30.0378789421227,-92.86721621096019\n"
    )
    csv_example.write(
        "30.03811467808153,-92.86843682562265,30.03791228279507,-92.86720907194727\n"
    )
    csv_example.write(
        "30.03814498173742,-92.86844237100571,30.03794600661214,-92.86720200245374\n"
    )
    csv_example.write(
        "30.03817536147593,-92.8684479304092,30.03798495119786,-92.86719775057487\n"
    )
    csv_example.write(
        "30.03821313704282,-92.86845282481077,30.03800676992721,-92.86719028007494\n"
    )
    csv_example.write(
        "30.03825342965967,-92.86847428143609,30.03803846552586,-92.86718833685659\n"
    )
    csv_example.write(
        "30.03827667158946,-92.8684805380621,30.038070336302,-92.86718638873742\n"
    )
    csv_example.write(
        "30.03831604066361,-92.86849386447184,30.03810236991961,-92.8671844310125\n"
    )
    csv_example.write(
        "30.03834805225929,-92.8685078614063,30.03812214148239,-92.86718218364435\n"
    )
    csv_example.write(
        "30.03839386704537,-92.86851230357081,30.03816179178459,-92.86717763639089\n"
    )
    csv_example.write(
        "30.03841988914808,-92.86853539844006,30.03818675848181,-92.86717816057062\n"
    )
    csv_example.write(
        "30.03845220839587,-92.86854953231291,30.0382094597554,-92.86718407029464\n"
    )
    csv_example.write(
        "30.03849208414191,-92.86856303294287,30.03825237810393,-92.8671877169286\n"
    )
    csv_example.seek(0)
    return centerline_width.riverCenterline(csv_data=csv_example)


river_class_example = river_class_object()


## riverFeatures() #####################################################
def test_riverCenterline_centerlineLength():
    assert river_class_example.centerlineLength == pytest.approx(
        0.08284102060354828)


def test_riverCenterline_rightBankLength():
    assert river_class_example.rightBankLength == pytest.approx(
        0.09705816897006408)


def test_riverCenterline_leftBankLength():
    assert river_class_example.leftBankLength == pytest.approx(
        0.10570962276643736)


def test_riverCenterline_area():
    assert river_class_example.area == pytest.approx(11.4030195647527)


def test_riverCenterline_riverSinuosity():
    assert river_class_example.sinuosity == pytest.approx(1.0124452966878812)


def test_riverCenterline_riverIncrementalSinuosity():
    assert river_class_example.incrementalSinuosity() == pytest.approx({
        ((-92.86781591391708, 30.038216571334427), (-92.8678415323492, 30.037979489365142)):
        1.0143354378572471,
        ((-92.86785143668344, 30.037954361467868), (-92.86793749224125, 30.03772716195012)):
        1.000273618506147
    })
