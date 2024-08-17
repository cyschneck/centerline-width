# Verify Outputs from plotDiagrams.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_verifyPlotDiagrams -xv

# Pytests to Compare and Verify Expected Outputs
from io import StringIO
import os
from pathlib import Path

# External Python libraries (installed via pip install)
import pytest
import matplotlib.testing.compare
import matplotlib.pyplot as plt

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

## Baseline plots generated generate_baseline_plots.py


def generate_testRiver():
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
    csv_example.write(
        "30.03852581421953,-92.86858562531111,30.03828804838585,-92.86719396008066\n"
    )
    csv_example.write(
        "30.03856087361126,-92.86861668659327,30.03832112388602,-92.86719194760462\n"
    )
    csv_example.write(
        "30.03858722679031,-92.86864003436845,30.03833392357112,-92.86719222755683\n"
    )
    csv_example.write(
        "30.03860731406331,-92.86867247414084,30.03839111275187,-92.86721003627284\n"
    )
    csv_example.write(
        "30.03863500018695,-92.86870434523594,30.03839638367213,-92.86721292131487\n"
    )
    csv_example.write(
        "30.03865515006033,-92.86873687804601,30.03843825552388,-92.86722222041689\n"
    )
    csv_example.write(
        "30.03868167793267,-92.86876041579589,30.03845130885886,-92.86722253452459\n"
    )
    csv_example.write(
        "30.03870950676927,-92.86879245332642,30.03848527029074,-92.8672205677704\n"
    )
    csv_example.write(
        "30.03872850322085,-92.86881666316253,30.03851698707168,-92.8672241164427\n"
    )
    csv_example.write(
        "30.03875766565788,-92.86885726630467,30.03854655211037,-92.86723326483309\n"
    )
    csv_example.write(
        "30.03877666276569,-92.86888148606303,30.03862026050065,-92.86726620967568\n"
    )
    csv_example.write(
        "30.03880571581789,-92.86892199098078,30.03865632342846,-92.86727869796846\n"
    )
    csv_example.write(
        "30.03881057580054,-92.86895573904928,30.03868457907467,-92.86729387294024\n"
    )
    csv_example.write(
        "30.03883200000636,-92.86899686713974,30.03870921964943,-92.86730024269222\n"
    )
    csv_example.write(
        "30.03884461187669,-92.86903019245257,30.03875072670094,-92.86731568609291\n"
    )
    csv_example.write(
        "30.03886511195148,-92.86906324319553,30.03877564654279,-92.86732213791971\n"
    )
    csv_example.write(
        "30.03889339091125,-92.86909588775821,30.03880067051145,-92.86732861661189\n"
    )
    csv_example.write(
        "30.03891395928556,-92.8691290392502,30.03883147361094,-92.86733817362666\n"
    )
    csv_example.write(
        "30.03894219332696,-92.86916164440944,30.03890252651567,-92.86739112760645\n"
    )
    csv_example.write(
        "30.03895365145345,-92.86918664981395,30.03892714061405,-92.86740169386835\n"
    )
    csv_example.write(
        "30.03897536669806,-92.86922822573946,30.03895191306113,-92.8674123035866\n"
    )
    csv_example.write(
        "30.03899596255844,-92.86926145558016,30.03896435523498,-92.86741762727362\n"
    )
    csv_example.write(
        "30.03900888702535,-92.86929526208631,30.03898718424111,-92.86744436767843\n"
    )
    csv_example.write(
        "30.03901274608691,-92.86932094789329,30.03900597663849,-92.86745814130126\n"
    )
    csv_example.write(
        "30.03902696879657,-92.86936335533146,30.03903117870811,-92.86748038378246\n"
    )
    csv_example.write(
        "30.03903211680724,-92.86939761958632,30.0390692546796,-92.86750830934984\n"
    )
    csv_example.write(
        "30.03904764079987,-92.86944864349289,30.03909483994374,-92.86753089868694\n"
    )
    csv_example.write(
        "30.03905407974185,-92.86949149646611,30.03912920549564,-92.86755739071201\n"
    )
    csv_example.write(
        "30.03906567618592,-92.86951676053803,30.03916167329965,-92.86757734744737\n"
    )
    csv_example.write(
        "30.03907198862608,-92.86955947122379,30.0391879094806,-92.86761206756863\n"
    )
    csv_example.write(
        "30.03907956369222,-92.8696107239798,30.0392208857466,-92.86764410816275\n"
    )
    csv_example.write(
        "30.03908587636264,-92.86965343442992,30.0392630032826,-92.86768036285451\n"
    )
    csv_example.write(
        "30.03909471412766,-92.8697132296213,30.03928758908551,-92.86769714757115\n"
    )
    csv_example.write(
        "30.03909976392995,-92.86974739852738,30.03932802154535,-92.86771507520557\n"
    )
    csv_example.write(
        "30.03909698994024,-92.86978183679166,30.03938694645366,-92.86774126455028\n"
    )
    csv_example.write(
        "30.03910203828103,-92.86981599450749,30.03942101877742,-92.86775053854353\n"
    )
    csv_example.write(
        "30.03910052718155,-92.86985893625713,30.03947614245786,-92.86777519127938\n"
    )
    csv_example.write(
        "30.03910557386241,-92.86989308263631,30.0394946684683,-92.8677834669401\n"
    )
    csv_example.write(
        "30.03911062018326,-92.86992722928346,30.03952488470748,-92.86779087708544\n"
    )
    csv_example.write(
        "30.03911945207219,-92.86998698601275,30.03955774739142,-92.86780548601331\n"
    )
    csv_example.write(
        "30.03912576049705,-92.87002966931057,30.03960283089936,-92.86783161618325\n"
    )
    csv_example.write(
        "30.03912424189665,-92.87007252734911,30.03961711466036,-92.86783797465486\n"
    )
    csv_example.write(
        "30.0391227243192,-92.87011535793397,30.03963622410157,-92.86784648143612\n"
    )
    csv_example.write(
        "30.03912776760816,-92.8701494826617,30.03966328550484,-92.86787679319379\n"
    )
    csv_example.write(
        "30.03911839757744,-92.87019235655339,30.03968306320493,-92.86789783995742\n"
    )
    csv_example.write(
        "30.03911677344246,-92.87023494412877,30.03969579570697,-92.86792196091567\n"
    )
    csv_example.write(
        "30.03912172468002,-92.8702689026297,30.03971575606928,-92.86794321684663\n"
    )
    csv_example.write(
        "30.03911105592404,-92.87030305839299,30.03975685348629,-92.86801128945807\n"
    )
    csv_example.write(
        "30.03911067303312,-92.87035403989468,30.03977445407076,-92.86802549334332\n"
    )
    csv_example.write(
        "30.03910937876896,-92.87039702701047,30.03979438501045,-92.86803454048447\n"
    )
    csv_example.write(
        "30.03909243695339,-92.87043998613844,30.03982400803992,-92.86803544226025\n"
    )
    csv_example.write(
        "30.0390832367404,-92.87048270589699,30.03985564110056,-92.86801835281109\n"
    )
    csv_example.write(
        "30.03908826030524,-92.87051669949084,30.03988785878878,-92.86801396556025\n"
    )
    csv_example.write(
        "30.03909579742933,-92.87056768999723,30.03992630834446,-92.8680374876463\n"
    )
    csv_example.write(
        "30.03910458827101,-92.87062717807787,30.03995195068288,-92.86804898205951\n"
    )
    csv_example.write(
        "30.03910057219471,-92.87065266047445,30.03997023211907,-92.8680635184745\n"
    )
    csv_example.write(
        "30.03910684992285,-92.87069513911989,30.03998858894517,-92.86807811485392\n"
    )
    csv_example.write(
        "30.03909882137005,-92.87074602755715,30.0400000132067,-92.8681087345056\n"
    )
    csv_example.write(
        "30.03909606509405,-92.87077993470241,30.04000571575267,-92.86812409286011\n"
    )
    csv_example.write(
        "30.03908554377088,-92.87081375579798,30.04001753990794,-92.8681679679199\n"
    )
    csv_example.write(
        "30.03906853476852,-92.87085593187457,30.04001801510858,-92.86818104448764\n"
    )
    csv_example.write(
        "30.03905805214026,-92.87088964999604,30.04002704858947,-92.8682174217282\n"
    )
    csv_example.write(
        "30.03904757866825,-92.87092332470544,30.04003087346458,-92.86825150611507\n"
    )
    csv_example.write(
        "30.0390448481104,-92.87095706654783,30.04004571957029,-92.86830385273672\n"
    )
    csv_example.write(
        "30.03904211881091,-92.87099078707058,30.0400649252065,-92.8683324411857\n"
    )
    csv_example.write(
        "30.03903939147361,-92.87102448540725,30.04007891343865,-92.86835865954328\n"
    )
    csv_example.write(
        "30.03904438937907,-92.87105830516076,30.04009776950889,-92.86837415603131\n"
    )
    csv_example.write(
        "30.0390446202305,-92.87116433856652,30.04012743931716,-92.86839480861163\n"
    )
    csv_example.write(
        "30.03904091120966,-92.87119129688267,30.04013817356334,-92.86839990875252\n"
    )
    csv_example.write(
        "30.03904219484274,-92.87125201062871,30.04015672997623,-92.8684021322278\n"
    )
    csv_example.write(
        "30.03904968114703,-92.87130267118744,30.04018017813587,-92.86839345241921\n"
    )
    csv_example.seek(0)

    return centerline_width.riverCenterline(csv_data=csv_example)


test_river = generate_testRiver()


@pytest.fixture(scope="session")
def generate_plot_image(tmp_path_factory):
    plt_file_path = tmp_path_factory.mktemp("data") / "pytest.png"
    return plt_file_path


################### plot_centerline() ##########################################################


def test_plotCenterline_darkMode_false(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               dark_mode=False,
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath('baseline_plots',
                                                    "dark_mode_false.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_darkMode_true(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               dark_mode=True,
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath('baseline_plots',
                                                    "dark_mode_true.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_displayAllPossiblePaths_false(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               display_all_possible_paths=False,
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "display_all_possible_paths_false.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_displayVoronoiGraph_false(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               display_voronoi=False,
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "display_voronoi_graph_false.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_displayAllPossiblePaths_true(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               display_all_possible_paths=True,
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "display_all_possible_paths_true.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_displayVoronoiGraph_true(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               display_voronoi=True,
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "display_voronoi_graph_true.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_equalAxis_false(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               equal_axis=False,
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath('baseline_plots',
                                                    "equal_axis_false.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_equalAxis_true(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               equal_axis=True,
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath('baseline_plots',
                                                    "equal_axis_true.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_equalDistance_decimalDegrees_line(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Equal Distance",
                               centerline_color="mediumorchid",
                               coordinate_unit="Decimal Degrees",
                               marker_type="Line",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "equal_distance_decimal_degrees_line.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_equalDistance_decimalDegrees_scatter(
        generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Equal Distance",
                               centerline_color="mediumorchid",
                               coordinate_unit="Decimal Degrees",
                               marker_type="Scatter",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "equal_distance_decimal_degrees_scatter.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_equalDistance_relativeDistance_line(
        generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Equal Distance",
                               centerline_color="mediumorchid",
                               coordinate_unit="Relative Distance",
                               marker_type="Line",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "equal_distance_relative_distance_line.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_equalDistance_relativeDistance_scatter(
        generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Equal Distance",
                               centerline_color="mediumorchid",
                               coordinate_unit="Relative Distance",
                               marker_type="Scatter",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "equal_distance_relative_distance_scatter.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_evenlySpaced_decimalDegrees_line(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Evenly Spaced",
                               centerline_color="fuchsia",
                               coordinate_unit="Decimal Degrees",
                               marker_type="Line",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "evenly_spaced_decimal_degrees_line.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_evenlySpaced_decimalDegrees_scatter(
        generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Evenly Spaced",
                               centerline_color="fuchsia",
                               coordinate_unit="Decimal Degrees",
                               marker_type="Scatter",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "evenly_spaced_decimal_degrees_scatter.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_evenlySpaced_relativeDistance_line(
        generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Evenly Spaced",
                               centerline_color="fuchsia",
                               coordinate_unit="Relative Distance",
                               marker_type="Line",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "evenly_spaced_relative_distance_line.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_evenlySpaced_relativeDistance_scatter(
        generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Evenly Spaced",
                               centerline_color="fuchsia",
                               coordinate_unit="Relative Distance",
                               marker_type="Scatter",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "evenly_spaced_relative_distance_scatter.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_smoothed_decimalDegrees_line(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Smoothed",
                               centerline_color="blue",
                               coordinate_unit="Decimal Degrees",
                               marker_type="Line",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "smoothed_decimal_degrees_line.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_smoothed_decimalDegrees_scatter(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Smoothed",
                               centerline_color="blue",
                               coordinate_unit="Decimal Degrees",
                               marker_type="Scatter",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "smoothed_decimal_degrees_scatter.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_smoothed_relativeDistance_line(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Smoothed",
                               centerline_color="blue",
                               coordinate_unit="Relative Distance",
                               marker_type="Line",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "smoothed_relative_distance_line.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_smoothed_relativeDistance_scatter(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Smoothed",
                               centerline_color="blue",
                               coordinate_unit="Relative Distance",
                               marker_type="Scatter",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "smoothed_relative_distance_scatter.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_voronoi_decimalDegrees_line(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Voronoi",
                               centerline_color="Black",
                               coordinate_unit="Decimal Degrees",
                               marker_type="Line",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "voronoi_decimal_degrees_line.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_voronoi_decimalDegrees_scatter(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Voronoi",
                               centerline_color="Black",
                               coordinate_unit="Decimal Degrees",
                               marker_type="Scatter",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "voronoi_decimal_degrees_scatter.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_voronoi_relativeDistance_line(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Voronoi",
                               centerline_color="Black",
                               coordinate_unit="Relative Distance",
                               marker_type="Line",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "voronoi_relative_distance_line.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterline_voronoi_relativeDistance_scatter(generate_plot_image):
    test_river.plot_centerline(save_plot_name=str(generate_plot_image),
                               centerline_type="Voronoi",
                               centerline_color="Black",
                               coordinate_unit="Relative Distance",
                               marker_type="Scatter",
                               show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "voronoi_relative_distance_scatter.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


################### plot_centerline_width() ########################################################


def test_plotCenterlineWidth_decimalDegrees_removeIntersectionsFalse_smoothedFalse_transectSlopeAverage(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Decimal Degrees",
                                     remove_intersections=False,
                                     apply_smoothing=False,
                                     transect_slope="Average",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_decimal_degrees_removeIntersectionsFalse_smoothedFalse_transectSlopeAverage.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_decimalDegrees_removeIntersectionsFalse_smoothedFalse_transectSlopeDirect(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Decimal Degrees",
                                     remove_intersections=False,
                                     apply_smoothing=False,
                                     transect_slope="Direct",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_decimal_degrees_removeIntersectionsFalse_smoothedFalse_transectSlopeDirect.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_decimalDegrees_removeIntersectionsFalse_smoothedTrue_transectSlopeAverage(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Decimal Degrees",
                                     remove_intersections=False,
                                     apply_smoothing=True,
                                     transect_slope="Average",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_decimal_degrees_removeIntersectionsFalse_smoothedTrue_transectSlopeAverage.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_decimalDegrees_removeIntersectionsFalse_smoothedTrue_transectSlopeDirect(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Decimal Degrees",
                                     remove_intersections=False,
                                     apply_smoothing=True,
                                     transect_slope="Direct",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_decimal_degrees_removeIntersectionsFalse_smoothedTrue_transectSlopeDirect.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_decimalDegrees_removeIntersectionsTrue_smoothedFalse_transectSlopeAverage(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Decimal Degrees",
                                     remove_intersections=True,
                                     apply_smoothing=False,
                                     transect_slope="Average",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_decimal_degrees_removeIntersectionsTrue_smoothedFalse_transectSlopeAverage.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_decimalDegrees_removeIntersectionsTrue_smoothedFalse_transectSlopeDirect(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Decimal Degrees",
                                     remove_intersections=True,
                                     apply_smoothing=False,
                                     transect_slope="Direct",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_decimal_degrees_removeIntersectionsTrue_smoothedFalse_transectSlopeDirect.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_decimalDegrees_removeIntersectionsTrue_smoothedTrue_transectSlopeAverage(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Decimal Degrees",
                                     remove_intersections=True,
                                     apply_smoothing=True,
                                     transect_slope="Average",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_decimal_degrees_removeIntersectionsTrue_smoothedTrue_transectSlopeAverage.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_decimalDegrees_removeIntersectionsTrue_smoothedTrue_transectSlopeDirect(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Decimal Degrees",
                                     remove_intersections=True,
                                     apply_smoothing=True,
                                     transect_slope="Direct",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_decimal_degrees_removeIntersectionsTrue_smoothedTrue_transectSlopeDirect.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_relativeDistance_removeIntersectionsFalse_smoothedFalse_transectSlopeAverage(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Relative Distance",
                                     remove_intersections=False,
                                     apply_smoothing=False,
                                     transect_slope="Average",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_relative_distance_removeIntersectionsFalse_smoothedFalse_transectSlopeAverage.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_relativeDistance_removeIntersectionsFalse_smoothedFalse_transectSlopeDirect(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Relative Distance",
                                     remove_intersections=False,
                                     apply_smoothing=False,
                                     transect_slope="Direct",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_relative_distance_removeIntersectionsFalse_smoothedFalse_transectSlopeDirect.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_relativeDistance_removeIntersectionsFalse_smoothedTrue_transectSlopeAverage(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Relative Distance",
                                     remove_intersections=False,
                                     apply_smoothing=True,
                                     transect_slope="Average",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_relative_distance_removeIntersectionsFalse_smoothedTrue_transectSlopeAverage.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_relativeDistance_removeIntersectionsFalse_smoothedTrue_transectSlopeDirect(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Relative Distance",
                                     remove_intersections=False,
                                     apply_smoothing=True,
                                     transect_slope="Direct",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_relative_distance_removeIntersectionsFalse_smoothedTrue_transectSlopeDirect.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_relativeDistance_removeIntersectionsTrue_smoothedFalse_transectSlopeAverage(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Relative Distance",
                                     remove_intersections=True,
                                     apply_smoothing=False,
                                     transect_slope="Average",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_relative_distance_removeIntersectionsTrue_smoothedFalse_transectSlopeAverage.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_relativeDistance_removeIntersectionsTrue_smoothedFalse_transectSlopeDirect(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Relative Distance",
                                     remove_intersections=True,
                                     apply_smoothing=False,
                                     transect_slope="Direct",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_relative_distance_removeIntersectionsTrue_smoothedFalse_transectSlopeDirect.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_relativeDistance_removeIntersectionsTrue_smoothedTrue_transectSlopeAverage(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Relative Distance",
                                     remove_intersections=True,
                                     apply_smoothing=True,
                                     transect_slope="Average",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_relative_distance_removeIntersectionsTrue_smoothedTrue_transectSlopeAverage.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_relativeDistance_removeIntersectionsTrue_smoothedTrue_transectSlopeDirect(
        generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     coordinate_unit="Relative Distance",
                                     remove_intersections=True,
                                     apply_smoothing=True,
                                     transect_slope="Direct",
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots',
        "width_relative_distance_removeIntersectionsTrue_smoothedTrue_transectSlopeDirect.png"
    )
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_displayCenterline_false(generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     display_true_centerline=False,
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "width_displayCenterlineFalse.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_displayCenterline_true(generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     display_true_centerline=True,
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "width_displayCenterlineTrue.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_flagIntersections_false(generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     flag_intersections=False,
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "width_flagIntersectionsFalse.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_flagIntersections_true(generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     flag_intersections=True,
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "width_flagIntersectionsTrue.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_darkMode_false(generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     dark_mode=False,
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "width_isDarkModeFalse.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_darkMode_true(generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     dark_mode=True,
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "width_isDarkModeTrue.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_equalAxis_false(generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     equal_axis=False,
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "width_isEqualAxisFalse.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None


def test_plotCenterlineWidth_equalAxis_true(generate_plot_image):
    test_river.plot_centerline_width(save_plot_name=str(generate_plot_image),
                                     equal_axis=True,
                                     show_plot=False)
    expected_png = (Path(__file__).parent).joinpath(
        'baseline_plots', "width_isEqualAxisTrue.png")
    plt.close()
    assert os.path.exists(expected_png)
    assert matplotlib.testing.compare.compare_images(
        expected_png, str(generate_plot_image), tol=0.001,
        in_decorator=False) is None
