# Dummy test for setting up circle.

def test_import():

    try:
        import tsar
    except ImportError:
        print("error importing package")
    assert True