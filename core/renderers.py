from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context.get(
            "response_data",
            renderer_context['response'].status_code
        )
        message = renderer_context.get(
            "message",
            renderer_context['response'].status_code
        )
        response_dict = {
          "message": message,
          "status": "success",
          "code": status_code,
          "data": data,
        }
        if "page_info" in data:
            page_info = data.pop("page_info")
            response_dict["page_info"] = page_info

        if not str(status_code).startswith('2'):
            response_dict["status"] = "error"
            response_dict["data"] = None
            try:
                response_dict["message"] = data["message"]
            except KeyError:
                response_dict["data"] = data

        return super(
            CustomRenderer, self
        ).render(response_dict, accepted_media_type, renderer_context)
