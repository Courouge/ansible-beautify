#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎨 Ansible Beautify Backend API

Modern Flask API for transforming one-liner Ansible tasks into beautiful YAML format.
Supports all Ansible modules with proper error handling and logging.

Author: Florian Courouge
Version: 1.0.0
"""

import os
import sys
import json
import logging
import re
import yaml
from io import StringIO
from pathlib import Path
from typing import Dict, List, Union, Any

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, InternalServerError

try:
    from ansible.errors import AnsibleParserError
    from ansible.parsing.mod_args import ModuleArgsParser
    from ansible.plugins.loader import module_loader
except ImportError:
    print("❌ Ansible not found. Please install: pip install ansible-core")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

class AnsibleBeautifier:
    """Main class for beautifying Ansible tasks using native Ansible parser."""
    
    def __init__(self, modules_file: str = "modules.txt"):
        """Initialize with modules file."""
        self.modules_file = Path(modules_file)
        self.modules = self._load_modules()
        logger.info(f"📦 Loaded {len(self.modules)} Ansible modules")
    
    def _load_modules(self) -> List[str]:
        """Load supported Ansible modules from file."""
        try:
            if not self.modules_file.exists():
                logger.warning(f"⚠️ Modules file {self.modules_file} not found")
                return []
            
            with open(self.modules_file, 'r', encoding='utf-8') as f:
                modules = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            # Sort modules by length (descending) to avoid short modules being masked by longer ones
            # e.g., 'copy' should be found before 'ce_file_copy' when looking for 'copy: ...'
            modules.sort(key=len, reverse=True)
            
            return modules
        except Exception as e:
            logger.error(f"❌ Error loading modules: {e}")
            return []
    
    def _parse_task_line(self, line: str) -> Dict[str, Any]:
        """Parse a task line using fallback and native Ansible parser."""
        line = line.strip()
        logger.info(f"🔍 Parsing line: '{line}'")
        
        # Find module in line - use regex for exact matching
        import re
        for module_name in self.modules:
            # Use regex to find exact module name followed by colon
            # This prevents 'copy' from matching 'ce_file_copy'
            pattern = rf'(?:^|\s)({re.escape(module_name)}):\s*'
            match = re.search(pattern, line)
            
            if match:
                logger.info(f"📦 Found exact module match: {module_name}")
                try:
                    # Extract prefix and parameters
                    module_start = match.start(1)
                    colon_pos = match.end()
                    
                    prefix = line[:module_start]
                    params_str = line[colon_pos:].strip()
                    logger.info(f"🎯 Module: {module_name}, Prefix: '{prefix}', Params: '{params_str}'")
                    
                    if not params_str:
                        # Just module name, no parameters
                        logger.info(f"✅ Module {module_name} with no parameters")
                        return {
                            'module': module_name,
                            'args': {},
                            'prefix': prefix,
                            'success': True
                        }
                    
                    # Try simple parsing first (more reliable)
                    args = self._simple_parse_params(params_str)
                    if args:
                        logger.info(f"✅ Successfully parsed {module_name} with simple parser")
                        return {
                            'module': module_name,
                            'args': args,
                            'prefix': prefix,
                            'success': True
                        }
                    
                    # Fallback to Ansible parser for complex cases
                    try:
                        task_dict = {module_name: params_str}
                        parser = ModuleArgsParser(task_dict)
                        module, parsed_args = parser.parse()
                        
                        if module and parsed_args:
                            logger.info(f"✅ Successfully parsed {module_name} with Ansible parser")
                            return {
                                'module': module,
                                'args': parsed_args,
                                'prefix': prefix,
                                'success': True
                            }
                    except Exception as e:
                        logger.debug(f"Ansible parser failed for {module_name}: {e}")
                        
                except Exception as e:
                    logger.debug(f"Parsing failed for {module_name}: {e}")
                    continue
        
        logger.warning(f"❌ No module found in line: '{line}'")
        return {'success': False, 'original_line': line}
    
    def _simple_parse_params(self, params_str: str) -> Dict[str, str]:
        """Simple fallback parameter parsing for when ModuleArgsParser fails."""
        if not params_str:
            return {}
        
        params = {}
        # Split on spaces but respect quoted values
        import shlex
        try:
            # Use shlex to properly handle quoted strings
            tokens = shlex.split(params_str)
            for token in tokens:
                if '=' in token:
                    key, value = token.split('=', 1)
                    params[key.strip()] = value.strip()
        except:
            # Fallback to simple regex if shlex fails
            import re
            pattern = r'(\w+)=((?:"[^"]*"|\'[^\']*\'|[^\s]+))'
            matches = re.findall(pattern, params_str)
            for key, value in matches:
                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                params[key] = value
        
        return params
    
    def _format_yaml_task(self, module: str, args: Dict[str, Any], prefix: str = "") -> List[str]:
        """Format a parsed task into beautiful YAML."""
        lines = []
        
        # Add the module name
        lines.append(f"{prefix}{module}:")
        
        # Determine indentation
        base_indent = "  " if not prefix.strip() else "    "
        
        # Sort parameters for consistent output
        priority_params = ['state', 'name', 'dest', 'src', 'path', 'content', 'when', 'become']
        sorted_params = []
        
        # Add priority params first
        for param in priority_params:
            if param in args:
                sorted_params.append(param)
        
        # Add remaining params alphabetically
        remaining = sorted([p for p in args.keys() if p not in priority_params])
        sorted_params.extend(remaining)
        
        # Format each parameter
        for param in sorted_params:
            value = args[param]
            
            # Format the value properly
            if isinstance(value, str):
                # Handle Jinja2 templates
                if '{{' in value and '}}' in value:
                    lines.append(f"{base_indent}{param}: {value}")
                # Handle boolean strings
                elif value.lower() in ['true', 'false', 'yes', 'no']:
                    lines.append(f"{base_indent}{param}: {value}")
                # Handle numeric strings
                elif value.isdigit():
                    lines.append(f"{base_indent}{param}: {value}")
                # Handle paths and complex strings
                elif any(char in value for char in [' ', '/', ':', ';', '&', '|', '*', '?', '[', ']']):
                    # Use YAML quoting for complex strings
                    if '"' in value:
                        lines.append(f"{base_indent}{param}: '{value}'")
                    else:
                        lines.append(f"{base_indent}{param}: \"{value}\"")
                else:
                    lines.append(f"{base_indent}{param}: {value}")
            elif isinstance(value, (list, dict)):
                # Convert complex structures to YAML
                yaml_value = yaml.dump(value, default_flow_style=False).strip()
                if '\n' in yaml_value:
                    # Multi-line YAML
                    lines.append(f"{base_indent}{param}:")
                    for yaml_line in yaml_value.split('\n'):
                        if yaml_line.strip():
                            lines.append(f"{base_indent}  {yaml_line}")
                else:
                    lines.append(f"{base_indent}{param}: {yaml_value}")
            else:
                lines.append(f"{base_indent}{param}: {value}")
        
        return lines

    def beautify(self, ansible_text: str) -> Dict[str, Any]:
        """
        Transform Ansible tasks into beautiful YAML using native Ansible parser.
        
        Args:
            ansible_text: Raw Ansible task text
            
        Returns:
            Dict with 'success', 'result', and optional 'error' keys
        """
        logger.info(f"🚀 Processing request with {len(ansible_text)} characters")
        
        if not ansible_text or not ansible_text.strip():
            logger.info("❌ Empty input provided")
            return {
                "success": False,
                "error": "Empty input provided",
                "result": ""
            }
        
        try:
            lines = ansible_text.strip().split('\n')
            logger.info(f"📝 Processing {len(lines)} lines: {lines}")
            result_lines = []
            modules_processed = 0
            
            for line in lines:
                logger.info(f"🔄 Processing line: '{line}'")
                if not line.strip():
                    result_lines.append(line)
                    continue
                
                # Try to parse the line with Ansible's native parser
                parsed = self._parse_task_line(line)
                logger.info(f"📊 Parse result: {parsed}")
                
                if parsed.get('success'):
                    # Format the parsed task
                    formatted_lines = self._format_yaml_task(
                        parsed['module'], 
                        parsed['args'], 
                        parsed['prefix']
                    )
                    result_lines.extend(formatted_lines)
                    modules_processed += 1
                else:
                    # Keep original line if parsing failed
                    result_lines.append(line)
            
            result = '\n'.join(result_lines)
            logger.info(f"✅ Final result: '{result}'")
            
            return {
                "success": True,
                "result": result,
                "modules_processed": modules_processed,
                "parser": "native_ansible"
            }
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in beautify: {e}")
            return {
                "success": False,
                "error": f"Processing error: {str(e)}",
                "result": ""
            }

# Initialize beautifier
beautifier = AnsibleBeautifier()

@app.route('/api/', methods=['GET', 'POST'])
def api_main():
    """Main API endpoint for beautifying Ansible tasks."""
    
    if request.method == 'GET':
        return jsonify({
            "service": "Ansible Beautify API",
            "version": "2.0.0",
            "status": "running",
            "modules_loaded": len(beautifier.modules),
            "endpoints": {
                "POST /api/": "Beautify Ansible tasks",
                "GET /api/health": "Health check",
                "GET /api/modules": "List supported modules"
            }
        })
    
    # Handle POST requests
    try:
        if not request.is_json:
            raise BadRequest("Content-Type must be application/json")
        
        data = request.get_json()
        
        if not data or 'in' not in data:
            raise BadRequest("Missing 'in' field in request body")
        
        input_text = data['in']
        
        if not isinstance(input_text, str):
            raise BadRequest("'in' field must be a string")
        
        logger.info(f"🔄 Processing request with {len(input_text)} characters")
        
        # Process the Ansible text
        result = beautifier.beautify(input_text)
        
        # Return in legacy format for compatibility
        return jsonify({
            "out": result["result"]
        })
        
    except BadRequest as e:
        logger.warning(f"⚠️ Bad request: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"❌ Internal server error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "ansible-beautify-backend",
        "modules_loaded": len(beautifier.modules)
    })

@app.route('/api/modules', methods=['GET'])
def list_modules():
    """List all supported Ansible modules."""
    return jsonify({
        "modules": beautifier.modules,
        "count": len(beautifier.modules)
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": ["/api/", "/api/health", "/api/modules"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"❌ Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting Ansible Beautify Backend...")
    logger.info(f"📦 Modules loaded: {len(beautifier.modules)}")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
