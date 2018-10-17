def get_formatted_disaster_name(input_disaster):
    DISASTERS = {
        'chemical': 'Chemical',
        'coastal-storm': 'Coastal Storm',
        'dam-levee-break': 'Dam/Levee Break',
        'drought': 'Drought',
        'earthquake': 'Earthquake',
        'fire': 'Fire',
        'fishing-losses': 'Fishing Losses',
        'flood': 'Flood',
        'freezing': 'Freezing',
        'human-cause': 'Human Cause',
        'hurricane': 'Hurricane',
        'mud-landslide': 'Mud/Landslide',
        'other': 'Other',
        'severe-ice-storm': 'Severe Ice Storm',
        'severe-storm': 'Severe Storm(s)',
        'snow': 'Snow',
        'terrorist': 'Terrorist',
        'tornado': 'Tornado',
        'toxic-substances': 'Toxic Substances',
        'tsuanmi': 'Tsunami',
        'typhoon': 'Typhoon',
        'volcano': 'Volcano'
    }

    if input_disaster in DISASTERS:
        return DISASTERS[input_disaster]

    return False
