if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    # PRINT COUNTS OF RECORDS WITH 
    print(f"Preprocessing: rows with zero passengers:{data['passenger_count'].isin([0]).sum()}")

    # RETURN FILTERED DATA SET
    return data[data['passenger_count']>0]

@test
# CHECK THAT THERE ARE NO RECORDS WITH 0 PASSENGER COUNT
def test_output(output, *args):
    assert output['passenger_count'].isin([0]).sum() ==0, 'There are rides with zero passengers'

