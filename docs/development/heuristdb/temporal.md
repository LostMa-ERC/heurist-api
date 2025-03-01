# Temporal objects

Heurist features compound dates that offer rich metadata such as uncertainty and probability distribution. Users might know this feature as a "compound" date, which is how the widget calls it. Internally, Heurist refers to this as a "temporal" object.

## Heurist's types of temporal objects

### 1. Simple date

A user can enter a simple date either with just the date or with additional metadata. This choice impacts how the API returns the result.

When a user opens the `Simple Date` tab and saves only a date, no other metadata, the Heurist API return the date as the direct and only value of `"value"`. See the example below of a year being entered.


**API JSON response (`date, compound, simple date`)**

```json
{
    "dty_ID": 1111,
    "value": 1188,
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": "",
},
```

However, if the user enters a date and then attaches additional information, such as `"Circa / approximate"`, by clicking the radio buttons beside the date field in the compound date widget, the Heurist API returns a metadata map in `"value"`.

**API JSON response (`date, compound, simple date`)**

```json
{
    "dty_ID": 1111,
    "value": {
        "timestamp": {
            "in": "1188",
            "type": "s",
            "circa": true
        },
        "estMinDate": 1188,
        "estMaxDate": 1188,
    },
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": "",
},
```

In the example above, the API describes the simple date as a `"timestamp"`. Furthermore, it has been given the type `"s"`. This type indication means the timestamp is a simple date, as opposed to a radiometric date, which are of type `"c"` for carbon.

### Widget radio buttons & Heurist API response

If the user wants to add a degree of certainty to a simple date, they must select one of the radio buttons on the `Simple Date` widget.

#### Exact simple date

The default selection is `Exact`, which is implied in the API's response by the absence of additional metadata.

```json
"timestamp": {
    "in": "1188",
    "type": "s",
},
```

#### Circa date

If the user selects the `Circa / approximate` radio button, the Heurist API returns `"circa": true`.

```json
"timestamp": {
    "in": "1188",
    "type": "s",
    "circa": true
},
```

#### Before date

If the user selects the `Before` radio button, the Heurist API returns `"before": true`.

```json
"timestamp": {
    "in": "1188",
    "type": "s",
    "before": true
},
```

#### After date

If the user selects the `After` radio button, the Heurist API returns `"after": true`.

```json
"timestamp": {
    "in": "1188",
    "type": "s",
    "after": true
},
```

### 2. Simple range

**API JSON response (`date, compound, simple range`)**

```json
{
    "dty_ID": 1111,
    "value": {
        "start": {"earliest": "1120"},
        "end": {"latest": "1150"},
        "estMinDate": 1120,
        "estMaxDate": 1150.1231,
    },
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": "",
},
```

### 3. Fuzzy range

**API JSON response (`date, compound, fuzzy range`)**

```json
{
    "dty_ID": 1111,
    "value": {
        "start": {
            "earliest": "1180",
            "latest": "1231",
        },
        "end": {
            "latest": "1250",
            "earliest": "1246",
        },
        "estMinDate": 1180,
        "estMaxDate": 1250.1231,
    },
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": "",
},
```

### 4. Radiometric

This type of date is not fully tested. The `heurist` package will still search for values in `value.estMinDate` and `value.estMaxDate` to generate the parsed date column. And for the `_TEMPORAL` column, the `heurist` package will return the whole dictionary in `value`. However, specific support and further documentation has not been developped.

## Certainty, probability distribution

Users can measure (i) a date or date range's degree of certainty and (ii) a date range's probability distribution. Users see these two measurements' scales described with English terms, i.e. "Conjecture". However, the Heurist API returns a numeric translation.

To develop the Python `heurist` API client, we must understand how Heurist manages this metadata.

### (i) Determination

The compound widget allows users to specify how they have determined a date.

- Unknown
- Attested
- Conjecture
- Measurement

The meaning of each value should be determined by the Heurist users and can vary depending on the project.

As seen in Heurist's [source code](https://github.com/HeuristNetwork/heurist/blob/7f30fb367c8c7e553513db6f7f51164e38e16f7c/hserv/utilities/Temporal.php#L80-L85), Heurist maps these values to a 0-4 numeric scale.

**PHP source code (`heurist/hserv/utilities/Temporal.php`)**

```php
<?php

private $dictDetermination = array(
    0=>"Unknown",
    1=>"Attested",
    2=>"Conjecture",
    3=>"Measurement"
);
```

The Heurist API returns the numeric value. For example, if a user enters a date range, 1454-1456, and indicates that this range is a conjecture, the Heurist API will return this detail with the key-value pair `"determination": "2"`.

**API JSON response (`date, compound, simple range`)**

```json
{
    "dty_ID": 1111,
    "value": {
        "start": {"earliest": "1454"},
        "end": {"latest": "1456"},
        "determination": "2",
        "estMinDate": 1454,
        "estMaxDate": 1456.1231,
    },
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": "",
}
```

### (ii) Probability distribution

The compound widget allows users to specify how a date range represents a probability distribution.

- Flat
- Central
- Slow Start
- Slow Finish

For more information on the probability distribution of dates, see Peter Stokes's [paper](http://peterstokes.org/pubs/Stokes_digital_dating.pdf) on modelling uncertainty in temporal metadata.

As seen in Heurist's [source code](https://github.com/HeuristNetwork/heurist/blob/7f30fb367c8c7e553513db6f7f51164e38e16f7c/hserv/utilities/Temporal.php#L87-L92), Heurist maps these values to a 0-4 numeric scale.

**PHP source code (`heurist/hserv/utilities/Temporal.php`)**

```php
<?php

private $dictProfile = array(
    0=>"Flat",
    1=>"Central",
    2=>"Slow Start",
    3=>"Slow Finish"
);
```

Below, look at the example of a fuzzy date range. At its extremes, the uncertain date is between 1180 and 1250. However, it is more probable that the earliest date is likely in the middle between 1180 and 1231, meaning it has a `"Central"` probability distribution. The latest date is probably between 1246 and 1250, though more likely nearer to 1246 than 1250. It has a `"Slow Finish"` probability distribution.

**API JSON response (`date, compound, fuzzy range`)**

```json
{
    "dty_ID": 1111,
    "value": {
        "start": {
            "earliest": "1180",
            "latest": "1231",
            "profile": "1"
        },
        "end": {
            "latest": "1250",
            "earliest": "1246",
            "profile": "3"
        },
        "determination": "2",
        "estMinDate": 1180,
        "estMaxDate": 1250.1231,
    },
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": "",
},
```

Metadata about a date range's probability distribution can also be attached directly at the root of the detail's value. This occurs when the user enters a simple date range, as opposed to a fuzzy date range.

**API JSON response (`date, compound, simple range`)**

```json
{
    "dty_ID": 1111,
    "value": {
        "start": {"earliest": "1120"},
        "end": {"latest": "1150"},
        "profile": "1",
        "estMinDate": 1120,
        "estMaxDate": 1150.1231,
    },
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": "",
},
```

## Comments

Compound dates can also be saved with comments. The Heurist API returns this metadata at the root of the detail's value.

**API JSON response (`date, compound, simple date`)**

```json
{
    "dty_ID": 1111,
    "value": {
        "timestamp": {"in": "1188", "type": "s", "circa": true},
        "comment": "From Klein (1995)",
        "estMinDate": 1188,
        "estMaxDate": 1188,
    },
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": "",
},
```