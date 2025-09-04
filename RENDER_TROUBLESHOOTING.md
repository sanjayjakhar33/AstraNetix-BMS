# 🛠️ Render Deployment Troubleshooting Guide

Common issues and solutions when deploying AstraNetix BMS to Render.

## 🔧 Blueprint Configuration Issues

### Invalid Blueprint Syntax

**Problem**: Deployment fails with blueprint parsing errors
```
Error: Invalid service configuration
Error: Unknown service type 'pserv'
Error: Unknown service type 'redis'
```

**Solutions**:
1. **Use correct service types**:
   - ✅ Use `type: keyvalue` for Redis (not `type: redis`)
   - ✅ Define PostgreSQL in `databases:` section (not as `type: pserv`)
   - ✅ Use `runtime: python` and `runtime: static` (not `env:`)

2. **Ensure proper blueprint structure**:
   ```yaml
   services:
     - type: keyvalue  # For Redis
       name: my-redis
     - type: web       # For applications
       runtime: python # or static
   
   databases:         # Separate section for databases
     - name: my-postgres
   ```

3. **Add repository references**:
   ```yaml
   - type: web
     repo: https://github.com/YOUR_USERNAME/AstraNetix-BMS.git
   ```

## 🚨 Build Failures

### Backend Build Fails

**Problem**: `pip install` fails during backend build
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions**:
1. **Check Python version**: Ensure Render uses Python 3.11+
   ```bash
   # Add to render.yaml or service settings
   environment: python
   pythonVersion: "3.11"
   ```

2. **Update requirements.txt**: Remove problematic packages
   ```bash
   # Comment out if causing issues
   # python-cors==1.7.0  # This package doesn't exist
   ```

3. **Clear cache**: In Render dashboard → Service → Settings → Clear build cache

### Frontend Build Fails

**Problem**: `npm install` or `npm run build` fails
```
Error: Cannot find module 'react-scripts'
```

**Solutions**:
1. **Check Node.js version**: Ensure using Node 18+
   ```yaml
   # In render.yaml
   env: node
   nodeVersion: "18"
   ```

2. **Clear npm cache**: 
   ```bash
   # Update build command
   buildCommand: "npm ci --cache /tmp/.npm && npm run build"
   ```

3. **Check package.json**: Ensure all dependencies are listed
   ```json
   {
     "dependencies": {
       "react-scripts": "5.0.1"
     }
   }
   ```

## 🗄️ Database Connection Issues

### Cannot Connect to PostgreSQL

**Problem**: Backend logs show database connection errors
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions**:
1. **Check DATABASE_URL**: Ensure it's properly set from database service
   ```bash
   # In Render environment variables
   DATABASE_URL=${DATABASE_URL}  # Auto-filled by Render
   ```

2. **Verify database service**: Ensure PostgreSQL service is running and healthy

3. **Check network**: Database and backend should be in same region

### Database Migration Issues

**Problem**: Tables don't exist or schema is outdated
```
relation "users" does not exist
```

**Solutions**:
1. **Run manual migration**: Use Render shell access
   ```bash
   # In backend service shell
   cd /opt/render/project/src
   python -m alembic upgrade head
   ```

2. **Initialize database**: Run initial SQL scripts
   ```bash
   # Connect to database
   psql $DATABASE_URL
   
   # Run initial schema
   \i database/migrations/001_initial_schema.sql
   ```

## 🔴 Redis Connection Issues

### Redis Connection Timeout

**Problem**: Backend cannot connect to Redis
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Solutions**:
1. **Check REDIS_URL**: Verify environment variable
   ```bash
   # Should be auto-set by Render
   REDIS_URL=redis://red-xyz123:6379
   ```

2. **Verify Redis service**: Ensure Redis is running and accessible

3. **Update Redis configuration**: Check maxmemory settings
   ```bash
   # In Redis service settings
   maxmemoryPolicy: allkeys-lru
   ```

## 🌐 CORS Issues

### Frontend Cannot Connect to Backend

**Problem**: Browser console shows CORS errors
```
Access to fetch at 'https://backend.onrender.com' from origin 'https://frontend.onrender.com' has been blocked by CORS policy
```

**Solutions**:
1. **Update CORS_ORIGINS**: Include all frontend URLs
   ```bash
   # Backend environment variable
   CORS_ORIGINS=https://founder-portal.onrender.com,https://isp-portal.onrender.com,https://branch-portal.onrender.com,https://user-portal.onrender.com
   ```

2. **Check frontend API URL**: Ensure correct backend URL
   ```bash
   # Frontend environment variable
   REACT_APP_API_URL=https://your-backend.onrender.com/api
   ```

3. **Protocol mismatch**: Ensure both use HTTPS in production

## ⚡ Performance Issues

### Slow Service Response

**Problem**: Services are slow or timeout frequently

**Solutions**:
1. **Upgrade plan**: Free tier has resource limitations
   ```
   Free Tier: 512MB RAM, 0.1 CPU
   Starter: 1GB RAM, 0.5 CPU  
   Standard: 2GB RAM, 1 CPU
   ```

2. **Optimize backend**: Reduce worker count if memory limited
   ```bash
   # Start command
   uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
   ```

3. **Database optimization**: Add indexes for better performance
   ```sql
   CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
   CREATE INDEX CONCURRENTLY idx_bandwidth_created_at ON bandwidth_usage(created_at);
   ```

### Service Sleep (Free Tier)

**Problem**: Free tier services sleep after 15 minutes of inactivity

**Solutions**:
1. **Upgrade to paid plan**: Prevents service sleeping
2. **Use uptime monitoring**: External service to ping your app
3. **Implement health check endpoint**: Already included at `/health`

## 🔐 Environment Variables Issues

### Missing or Invalid Environment Variables

**Problem**: Service fails to start due to missing config
```
KeyError: 'DATABASE_URL'
```

**Solutions**:
1. **Check all required variables**: Refer to `.env.render` template
2. **Verify auto-generated variables**: Database and Redis URLs
3. **Generate secure secrets**: Use strong JWT keys
   ```bash
   # Generate JWT secret
   openssl rand -hex 32
   ```

### Secret Key Issues

**Problem**: JWT authentication fails
```
Invalid token or signature verification failed
```

**Solutions**:
1. **Use consistent JWT secret**: Same across all deployments
2. **Generate secure secret**: At least 32 characters
3. **Check algorithm**: Ensure HS256 is used

## 🔧 Service-Specific Issues

### Static Site Build Issues

**Problem**: React build produces errors or warnings treated as errors

**Solutions**:
1. **Disable warnings as errors**: Add to build command
   ```bash
   # Build command
   CI=false npm run build
   ```

2. **Fix TypeScript errors**: Address all TS compilation issues
3. **Update dependencies**: Ensure compatible versions

### Health Check Failures

**Problem**: Render marks service as unhealthy

**Solutions**:
1. **Check health endpoint**: Ensure `/health` returns 200
   ```bash
   curl https://your-backend.onrender.com/health
   ```

2. **Verify health check path**: In service settings
   ```
   Health Check Path: /health
   ```

3. **Increase timeout**: Some services need more time to start

## 📊 Monitoring and Debugging

### View Service Logs

1. **Render Dashboard**: Go to service → Logs tab
2. **Real-time logs**: Use the live log stream
3. **Filter logs**: Use search to find specific errors

### Check Service Metrics

1. **Performance**: CPU, Memory usage in dashboard
2. **Response times**: Monitor API response times
3. **Error rates**: Track 4xx/5xx responses

### Debug Environment

1. **Shell access**: Use Render shell to debug
   ```bash
   # In service shell
   env | grep DATABASE_URL
   python -c "import sqlalchemy; print('SQLAlchemy works')"
   ```

2. **Test connections**: Verify database and Redis connectivity
   ```bash
   # Test database
   psql $DATABASE_URL -c "SELECT version();"
   
   # Test Redis
   redis-cli -u $REDIS_URL ping
   ```

## 🆘 Getting Help

### Render Support Channels

1. **Documentation**: [render.com/docs](https://render.com/docs)
2. **Community**: [community.render.com](https://community.render.com)
3. **Support**: Through Render dashboard (paid plans)

### AstraNetix Support

1. **GitHub Issues**: [Create an issue](https://github.com/sanjayjakhar33/AstraNetix-BMS/issues)
2. **Include logs**: Share relevant error logs (without sensitive data)
3. **Deployment info**: Mention Render-specific details

### Common Error Patterns

| Error Pattern | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| `Module not found` | Missing dependency | Check package.json/requirements.txt |
| `Connection refused` | Service not running | Check service status |
| `CORS error` | Wrong origins | Update CORS_ORIGINS variable |
| `404 on API calls` | Wrong API URL | Check REACT_APP_API_URL |
| `Memory limit exceeded` | Insufficient resources | Upgrade plan |
| `Build timeout` | Slow build process | Optimize build commands |

## ✅ Success Checklist

When everything works correctly, you should see:

- ✅ All services show "Live" status in Render dashboard
- ✅ Backend API responds at `/health` and `/docs` endpoints  
- ✅ Frontend applications load without console errors
- ✅ Login functionality works across all portals
- ✅ Database connections are stable
- ✅ Redis caching is functional
- ✅ No CORS errors in browser console

Happy deploying! 🚀