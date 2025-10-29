from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .models import Blog
from django.db.models import Q


class BlogView(APIView):
    permission_classes = [IsAuthenticated]   
    authentication_classes = [JWTAuthentication]   
    
    def get(self, request, uid=None):
        try:
            # If uid is provided, get single blog
            if uid:
                try:
                    blog = Blog.objects.get(uid=uid, user=request.user)
                    serializer = BlogSerializer(blog)
                    return Response({
                        'data': serializer.data,
                        'message': 'Blog retrieved successfully',
                    }, status=status.HTTP_200_OK)
                except Blog.DoesNotExist:
                    return Response({
                        'data': {},
                        'message': 'Blog not found',
                    }, status=status.HTTP_404_NOT_FOUND)
            
            # Otherwise, get all blogs for the user
            blogs = Blog.objects.filter(user=request.user)
            
            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = blogs.filter(Q(title__icontains=search) | Q(Blog_text__icontains=search))
            
            serializer = BlogSerializer(blogs, many=True)
            return Response({
                'data': serializer.data,
                'message': 'Blogs retrieved successfully',
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):     
        try:
            data = request.data
            serializer = BlogSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save(user=request.user)
                
                return Response({
                    'data': serializer.data,
                    'message': 'Blog created successfully',
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'data': {},
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'data': {},
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, uid):
        """Update a blog - uid comes from URL path"""
        try:
            # Get the blog and verify ownership
            try:
                blog = Blog.objects.get(uid=uid, user=request.user)
            except Blog.DoesNotExist:
                return Response({
                    'data': {},
                    'message': 'Blog not found or you do not have permission to edit it',
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Update with new data (partial=True allows partial updates)
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'Blog updated successfully',
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'data': {},
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, uid):
        """Partial update - same as PUT in this case"""
        return self.put(request, uid)
    
    def delete(self, request, uid):
        """Delete a blog - uid comes from URL path"""
        try:
            # Get the blog and verify ownership
            try:
                blog = Blog.objects.get(uid=uid, user=request.user)
            except Blog.DoesNotExist:
                return Response({
                    'data': {},
                    'message': 'Blog not found or you do not have permission to delete it',
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Delete the blog
            blog.delete()
            
            return Response({
                'data': {},
                'message': 'Blog deleted successfully',
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)