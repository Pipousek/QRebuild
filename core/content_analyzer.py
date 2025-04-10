import json
from urllib.parse import urlparse

class ContentAnalyzer:
    @staticmethod
    def analyze(content):
        """Analyze QR code content and return structured information."""
        try:
            # 1. Check for empty content
            if not content.strip():
                return {
                    'type': 'Empty',
                    'data': {'message': 'No content detected'}
                }

            # 2. Check for URL
            parsed = urlparse(content)
            if parsed.scheme and parsed.netloc:
                return {
                    'type': 'URL',
                    'data': {
                        'scheme': parsed.scheme,
                        'domain': parsed.netloc,
                        'path': parsed.path or '/',
                        'query': parsed.query,
                        'fragment': parsed.fragment
                    }
                }

            # 3. Check for WiFi network configuration
            if content.startswith('WIFI:'):
                params = {}
                for part in content[5:].split(';'):
                    if ':' in part:
                        key, val = part.split(':', 1)
                        params[key] = val
                return {
                    'type': 'WiFi Configuration',
                    'data': {
                        'ssid': params.get('S', ''),
                        'password': bool(params.get('P')),
                        'encryption': params.get('T', 'Unknown'),
                        'hidden': params.get('H') == 'true'
                    }
                }

            # 4. Check for vCard
            if content.startswith('BEGIN:VCARD'):
                result = {'type': 'vCard', 'data': {}}
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('VERSION:'):
                        result['data']['version'] = line.split(':', 1)[1]
                    elif line.startswith('N:'):
                        name_parts = line.split(':', 1)[1].split(';')
                        result['data']['name_structured'] = {
                            'last': name_parts[0] if len(name_parts) > 0 else '',
                            'first': name_parts[1] if len(name_parts) > 1 else '',
                            'middle': name_parts[2] if len(name_parts) > 2 else '',
                            'prefix': name_parts[3] if len(name_parts) > 3 else '',
                            'suffix': name_parts[4] if len(name_parts) > 4 else ''
                        }
                    elif line.startswith('FN:'):
                        result['data']['name'] = line.split(':', 1)[1]
                    elif line.startswith('TITLE:'):
                        result['data']['title'] = line.split(':', 1)[1]
                    elif line.startswith('TEL:') or line.startswith('TEL;'):
                        # Handle phone with parameters like TEL;WORK;VOICE:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            phone_value = parts[1]
                            phone_type = parts[0].split(';')[1:] if ';' in parts[0] else ['DEFAULT']
                            result['data']['phone'] = phone_value
                            result['data']['phone_type'] = ';'.join(phone_type)
                    elif line.startswith('EMAIL:') or line.startswith('EMAIL;'):
                        # Handle email with parameters like EMAIL;WORK;INTERNET:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            email_value = parts[1]
                            email_type = parts[0].split(';')[1:] if ';' in parts[0] else ['DEFAULT']
                            result['data']['email'] = email_value
                            result['data']['email_type'] = ';'.join(email_type)
                    elif line.startswith('ORG:'):
                        result['data']['organization'] = line.split(':', 1)[1]
                    elif line.startswith('ADR:') or line.startswith('ADR;'):
                        # Handle address with parameters
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            addr_parts = parts[1].split(';')
                            addr_type = parts[0].split(';')[1:] if ';' in parts[0] else ['DEFAULT']
                            result['data']['address'] = {
                                'po_box': addr_parts[0] if len(addr_parts) > 0 else '',
                                'extended': addr_parts[1] if len(addr_parts) > 1 else '',
                                'street': addr_parts[2] if len(addr_parts) > 2 else '',
                                'city': addr_parts[3] if len(addr_parts) > 3 else '',
                                'region': addr_parts[4] if len(addr_parts) > 4 else '',
                                'postal': addr_parts[5] if len(addr_parts) > 5 else '',
                                'country': addr_parts[6] if len(addr_parts) > 6 else '',
                                'type': ';'.join(addr_type)
                            }
                    elif line.startswith('URL:'):
                        result['data']['url'] = line.split(':', 1)[1]
                    elif line.startswith('NOTE:'):
                        result['data']['note'] = line.split(':', 1)[1]
                return result

            # 5. Check for Bitcoin address
            if content.lower().startswith('bitcoin:'):
                addr = content[8:].split('?')[0]
                result = {
                    'type': 'Bitcoin Payment',
                    'data': {
                        'address': addr
                    }
                }
                if '?' in content:
                    params = content.split('?')[1]
                    for param in params.split('&'):
                        if '=' in param:
                            key, val = param.split('=', 1)
                            result['data'][key.lower()] = val
                return result

            # 6. Check for JSON
            try:
                json_data = json.loads(content)
                return {
                    'type': 'JSON',
                    'data': json_data
                }
            except:
                pass

            # 7. Check for email
            if '@' in content and '\n' not in content:
                if content.lower().startswith('mailto:'):
                    try:
                        # Format: mailto:address?param1=value1&param2=value2
                        parts = content[7:].split('?', 1)  # Split at first ?
                        address = parts[0]
                        params = {}
                        
                        if len(parts) > 1:
                            for param in parts[1].split('&'):
                                if '=' in param:
                                    key, val = param.split('=', 1)
                                    params[key.lower()] = val
                        
                        return {
                            'type': 'Email',
                            'data': {
                                'address': address,
                                'parameters': params
                            }
                        }
                    except Exception as e:
                        return {
                            'type': 'Error',
                            'data': {
                                'message': f"Invalid mailto format: {str(e)}"
                            }
                        }
                elif ' ' not in content and '.' in content.split('@')[-1]:
                    return {
                        'type': 'Email',
                        'data': {
                            'address': content,
                            'parameters': {}
                        }
                    }

            # 8. Check for phone number
            if (content.replace('+', '').replace(' ', '').isdigit() and 
                len(content.replace(' ', '')) > 6):
                if content.startswith('tel:'):
                    return {
                        'type': 'Phone',
                        'data': {
                            'number': content[4:]
                        }
                    }
                else:
                    return {
                        'type': 'Phone',
                        'data': {
                            'number': content
                        }
                    }

            # 9. Check for SMS
            if content.lower().startswith('smsto:'):
                parts = content[6:].split(':')
                result = {
                    'type': 'SMS',
                    'data': {
                        'number': parts[0]
                    }
                }
                if len(parts) > 1:
                    result['data']['message'] = parts[1]
                return result
            
            # 2. Check for GEO location
            if content.lower().startswith('geo:'):
                try:
                    # Format: geo:lat,lng[,alt][;param=value]
                    parts = content[4:].split(';')
                    coordinates = parts[0].split(',')
                    
                    data = {
                        'latitude': float(coordinates[0]),
                        'longitude': float(coordinates[1]),
                        'altitude': float(coordinates[2]) if len(coordinates) > 2 else None
                    }
                    
                    # Parse parameters if any
                    if len(parts) > 1:
                        params = {}
                        for param in parts[1:]:
                            if '=' in param:
                                key, val = param.split('=', 1)
                                params[key.lower()] = val
                        data['parameters'] = params
                    
                    return {
                        'type': 'Geographic Location',
                        'data': data
                    }
                except Exception as e:
                    return {
                        'type': 'Error',
                        'data': {
                            'message': f"Invalid GEO format: {str(e)}"
                        }
                    }

            # 10. Default to plain text
            return {
                'type': 'Text',
                'data': {
                    'length': len(content),
                    'preview': content[:100] + ('...' if len(content) > 100 else '')
                }
            }

        except Exception as e:
            return {
                'type': 'Error',
                'data': {
                    'message': str(e)
                }
            }

    @staticmethod
    def format_structured_content(analysis):
        """Format the analysis result into human-readable text."""
        if analysis['type'] == 'Error':
            return f"Error analyzing content: {analysis['data']['message']}"

        lines = [f"Type: {analysis['type']}"]
        
        if analysis['type'] == 'URL':
            url_data = analysis['data']
            lines.append(f"Scheme: {url_data['scheme']}")
            lines.append(f"Domain: {url_data['domain']}")
            lines.append(f"Path: {url_data['path']}")
            if url_data['query']:
                lines.append(f"Query: {url_data['query']}")
            if url_data['fragment']:
                lines.append(f"Fragment: {url_data['fragment']}")

        elif analysis['type'] == 'WiFi Configuration':
            wifi_data = analysis['data']
            lines.append(f"SSID: {wifi_data['ssid']}")
            lines.append("Password: " + ("*****" if wifi_data['password'] else "(none)"))
            lines.append(f"Encryption: {wifi_data['encryption']}")
            lines.append(f"Hidden: {'Yes' if wifi_data['hidden'] else 'No'}")

        elif analysis['type'] == 'vCard':
            vcard_data = analysis['data']
            if 'version' in vcard_data:
                lines.append(f"Version: {vcard_data['version']}")
            if 'name' in vcard_data:
                lines.append(f"Full Name: {vcard_data['name']}")
            if 'name_structured' in vcard_data:
                ns = vcard_data['name_structured']
                name_parts = []
                if ns['prefix']: 
                    name_parts.append(ns['prefix'])
                if ns['first']: 
                    name_parts.append(ns['first'])
                if ns['middle']: 
                    name_parts.append(ns['middle'])
                if ns['last']: 
                    name_parts.append(ns['last'])
                if ns['suffix']: 
                    name_parts.append(ns['suffix'])
                lines.append(f"Name Structure: {', '.join(name_parts)}")
            if 'title' in vcard_data:
                lines.append(f"Title: {vcard_data['title']}")
            if 'organization' in vcard_data:
                lines.append(f"Organization: {vcard_data['organization']}")
            if 'phone' in vcard_data:
                phone_type = f" ({vcard_data['phone_type']})" if 'phone_type' in vcard_data else ""
                lines.append(f"Phone{phone_type}: {vcard_data['phone']}")
            if 'email' in vcard_data:
                email_type = f" ({vcard_data['email_type']})" if 'email_type' in vcard_data else ""
                lines.append(f"Email{email_type}: {vcard_data['email']}")
            if 'address' in vcard_data:
                addr = vcard_data['address']
                addr_type = f" ({addr['type']})" if 'type' in addr else ""
                addr_str = []
                if addr['street']: 
                    addr_str.append(addr['street'])
                if addr['city']: 
                    addr_str.append(addr['city'])
                if addr['region']: 
                    addr_str.append(addr['region'])
                if addr['postal']: 
                    addr_str.append(addr['postal'])
                if addr['country']: 
                    addr_str.append(addr['country'])
                lines.append(f"Address{addr_type}: {', '.join(addr_str)}")
            if 'url' in vcard_data:
                lines.append(f"URL: {vcard_data['url']}")
            if 'note' in vcard_data:
                lines.append(f"Note: {vcard_data['note']}")

        elif analysis['type'] == 'Bitcoin Payment':
            btc_data = analysis['data']
            lines.append(f"Address: {btc_data['address']}")
            for key, value in btc_data.items():
                if key != 'address':
                    lines.append(f"{key.capitalize()}: {value}")

        elif analysis['type'] == 'JSON':
            lines.append(json.dumps(analysis['data'], indent=2))

        elif analysis['type'] == 'Email':
            email_data = analysis['data']
            lines.append(f"Address: {email_data['address']}")
            
            # Format standard parameters
            param_map = {
                'subject': 'Subject',
                'body': 'Body',
                'cc': 'CC',
                'bcc': 'BCC',
                'to': 'To'
            }
            
            for param, value in email_data['parameters'].items():
                display_name = param_map.get(param, param.capitalize())
                if param == 'body':
                    # Handle body with potential newlines
                    lines.append(f"{display_name}:\n{value.replace('%0A', '\n')}")
                else:
                    lines.append(f"{display_name}: {value}")

        elif analysis['type'] in ['Email', 'Phone']:
            for key, value in analysis['data'].items():
                lines.append(f"{key.capitalize()}: {value}")

        elif analysis['type'] == 'SMS':
            sms_data = analysis['data']
            lines.append(f"Number: {sms_data['number']}")
            if 'message' in sms_data:
                lines.append(f"Message: {sms_data['message']}")

        elif analysis['type'] == 'Geographic Location':
            geo_data = analysis['data']
            lines.append(f"Latitude: {geo_data['latitude']}")
            lines.append(f"Longitude: {geo_data['longitude']}")
            if geo_data['altitude'] is not None:
                lines.append(f"Altitude: {geo_data['altitude']} meters")
            if 'parameters' in geo_data:
                for param, value in geo_data['parameters'].items():
                    lines.append(f"{param.capitalize()}: {value}")
            lines.append("\nGoogle Maps Link:")
            lines.append(f"https://www.google.com/maps?q={geo_data['latitude']},{geo_data['longitude']}")

        elif analysis['type'] == 'Text':
            text_data = analysis['data']
            lines.append(f"Length: {text_data['length']} characters")
            lines.append(f"Preview:\n{text_data['preview']}")

        elif analysis['type'] == 'Empty':
            lines.append(analysis['data']['message'])

        return '\n'.join(lines)