BASE = """
{imports}
export default function {function_name}() {{
{js_script}
    return (
{html_block}
        );
}}
"""


REACT_USE_STATE = """
    const [open, setOpen] = useState(false);
"""

HASHROUTER_IMPORT = "import { HashLink } from 'react-router-hash-link';"

REACT_IMPORT = """
import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Collapse from 'react-bootstrap/Collapse';
"""
