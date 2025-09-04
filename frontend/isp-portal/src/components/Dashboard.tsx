import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  Button,
  AppBar,
  Toolbar,
  IconButton,
  Menu,
  MenuItem
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Business as BusinessIcon,
  People as PeopleIcon,
  AttachMoney as MoneyIcon,
  Settings as SettingsIcon,
  AccountCircle
} from '@mui/icons-material';

interface DashboardData {
  total_isps: number;
  total_branches: number;
  total_users: number;
  monthly_revenue: number;
  system_health: number;
  recent_isps: any[];
}

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  useEffect(() => {
    // Mock data for demo
    setDashboardData({
      total_isps: 12,
      total_branches: 45,
      total_users: 1250,
      monthly_revenue: 125000,
      system_health: 99.9,
      recent_isps: [
        { id: '1', company_name: 'TechNet ISP', domain: 'technet', created_at: '2024-01-15' },
        { id: '2', company_name: 'FastConnect', domain: 'fastconnect', created_at: '2024-01-14' }
      ]
    });
  }, []);

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  if (!dashboardData) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <DashboardIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AstraNetix BMS - Founder Portal
          </Typography>
          <IconButton
            size="large"
            edge="end"
            aria-label="account of current user"
            aria-controls="primary-search-account-menu"
            aria-haspopup="true"
            onClick={handleProfileMenuOpen}
            color="inherit"
          >
            <AccountCircle />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={handleMenuClose}>Profile</MenuItem>
            <MenuItem onClick={handleMenuClose}>Settings</MenuItem>
            <MenuItem onClick={handleMenuClose}>Logout</MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard Overview
        </Typography>
        
        {/* Stats Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <BusinessIcon color="primary" sx={{ mr: 2, fontSize: 40 }} />
                  <Box>
                    <Typography color="text.secondary" gutterBottom>
                      Total ISPs
                    </Typography>
                    <Typography variant="h4">
                      {dashboardData.total_isps}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <BusinessIcon color="secondary" sx={{ mr: 2, fontSize: 40 }} />
                  <Box>
                    <Typography color="text.secondary" gutterBottom>
                      Total Branches
                    </Typography>
                    <Typography variant="h4">
                      {dashboardData.total_branches}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <PeopleIcon color="success" sx={{ mr: 2, fontSize: 40 }} />
                  <Box>
                    <Typography color="text.secondary" gutterBottom>
                      Total Users
                    </Typography>
                    <Typography variant="h4">
                      {dashboardData.total_users.toLocaleString()}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <MoneyIcon color="warning" sx={{ mr: 2, fontSize: 40 }} />
                  <Box>
                    <Typography color="text.secondary" gutterBottom>
                      Monthly Revenue
                    </Typography>
                    <Typography variant="h4">
                      ${dashboardData.monthly_revenue.toLocaleString()}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Recent Activity */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent ISPs
                </Typography>
                {dashboardData.recent_isps.map((isp) => (
                  <Box key={isp.id} sx={{ py: 1, borderBottom: '1px solid #eee' }}>
                    <Typography variant="body1" fontWeight="bold">
                      {isp.company_name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Domain: {isp.domain} | Created: {isp.created_at}
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  System Health
                </Typography>
                <Box textAlign="center">
                  <Typography variant="h2" color="success.main">
                    {dashboardData.system_health}%
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    All systems operational
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Quick Actions */}
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Quick Actions
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Button variant="contained" color="primary">
              Create New ISP
            </Button>
            <Button variant="outlined" color="primary">
              View Analytics
            </Button>
            <Button variant="outlined" color="secondary">
              System Monitoring
            </Button>
            <Button variant="outlined" startIcon={<SettingsIcon />}>
              Global Settings
            </Button>
          </Box>
        </Box>
      </Container>
    </>
  );
};

export default Dashboard;